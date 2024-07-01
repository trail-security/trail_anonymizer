import hashlib
import logging
import time
from collections import defaultdict
from typing import Optional, List, Dict, Any

import pandas as pd
from presidio_analyzer import AnalyzerEngine, BatchAnalyzerEngine, DictAnalyzerResult
from presidio_anonymizer import AnonymizerEngine, BatchAnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

logger = logging.getLogger("TrailSecurityAnonymizer")
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)


def hash_as_hex(string_to_hash: str, hash_length: int = 8) -> str:
    hash_object = hashlib.sha256(string_to_hash.encode())
    return hash_object.hexdigest()[:hash_length]


def fake_email(original_email: str) -> str:
    email_parts = original_email.split("@")
    if len(email_parts) != 2:
        hashed_email = hash_as_hex(original_email)
        return f"user_{hashed_email[:8]}@ts_example.com"

    email_prefix = email_parts[0]
    email_domain = email_parts[1]
    hashed_email_prefix = hash_as_hex(email_prefix)
    return f"user_{hashed_email_prefix}@{email_domain}"


class TrailAnonymizer:
    def __init__(self):
        self._analyzer = AnalyzerEngine()
        self._batch_analyzer = BatchAnalyzerEngine(analyzer_engine=self._analyzer)

        self._anonymizer = AnonymizerEngine()
        self._batch_anonymizer = BatchAnonymizerEngine()

    def run(
        self,
        path: str,
        *,
        columns_to_anonymize: Optional[List[str]] = None,
        entities: Optional[List[str]] = None,
    ):
        start = time.perf_counter()
        logger.info(f"Running TrailSecurityAnonymizer on '{path}'.")
        logger.info("------------------------------")

        file_format = path.split(".")[-1]
        if file_format == "csv":
            self._run_csv(path, columns_to_anonymize, entities)
        elif file_format == "xlsx":
            self._run_xlsx(path, columns_to_anonymize, entities)
        else:
            raise NotImplementedError(
                f"{file_format} file format is not supported yet."
            )

        end = time.perf_counter()
        logger.info(f"TrailSecurityAnonymizer completed in {end - start:0.3f} seconds.")

    def _run_csv(
        self,
        path: str,
        columns_to_anonymize: Optional[List[str]] = None,
        entities: Optional[List[str]] = None,
    ):
        df = pd.read_csv(path)
        scrubbed_df = self._run_sheet(
            df,
            columns_to_anonymize,
            entities,
        )
        logger.info("------------------------------")
        new_file_name = self._new_file_name(path)
        self._save_csv(scrubbed_df, new_file_name)

    def _run_xlsx(
        self,
        path: str,
        columns_to_anonymize: Optional[List[str]] = None,
        entities: Optional[List[str]] = None,
    ):
        scrubbed_sheets_dfs_map = {}
        sheets_list = pd.read_excel(path, sheet_name=None)
        for name, sheet in sheets_list.items():
            logger.info(f"Anonymizing sheet '{name}'.")
            scrubbed_sheet_df = self._run_sheet(sheet, columns_to_anonymize, entities)
            scrubbed_sheets_dfs_map[name] = scrubbed_sheet_df
            logger.info("------------------------------")

        new_file_name = self._new_file_name(path)
        writer = pd.ExcelWriter(new_file_name, engine="xlsxwriter")
        for sheet_name, sheet_df in scrubbed_sheets_dfs_map.items():
            sheet_df.to_excel(writer, sheet_name=sheet_name, startrow=0, startcol=0)

        writer.close()
        logger.info(f"Anonymized data saved to '{new_file_name}'.")

    def _run_sheet(
        self,
        df: pd.DataFrame,
        columns_to_anonymize: Optional[List[str]] = None,
        entities: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        start = time.perf_counter()
        df_dict = df.to_dict(orient="list")

        dataframe_columns_to_skip = (
            list(set(df.columns) - set(columns_to_anonymize))
            if columns_to_anonymize is not None
            else None
        )
        logger.info(
            f"Anonymizing columns: {columns_to_anonymize if columns_to_anonymize is not None else "ALL"}."
        )
        logger.info(
            f"Anonymizing entities: {entities if entities is not None else "ALL"}."
        )

        analyzer_results = self._analyze(df_dict, entities, dataframe_columns_to_skip)
        self._log_aggregate_results(analyzer_results)

        anonymizer_results = self._anonymize(analyzer_results, entities)

        scrubbed_df = pd.DataFrame(anonymizer_results)

        end = time.perf_counter()
        logger.info(f"Completed in {end - start:0.3f} seconds.")

        return scrubbed_df

    def _save_csv(self, df: pd.DataFrame, path: str):
        df.to_csv(path, index=False)
        logger.info(f"Anonymized data saved to '{path}'.")

    def _analyze(
        self,
        df_dict: Dict[str, List[str]],
        entities: List[str],
        dataframe_columns_to_skip: List[str],
    ) -> List[DictAnalyzerResult]:
        analyzer_results = self._batch_analyzer.analyze_dict(
            df_dict,
            language="en",
            entities=entities,
            keys_to_skip=dataframe_columns_to_skip,
        )
        analyzer_results_list = list(analyzer_results)
        return analyzer_results_list

    def _anonymize(
        self, analyzer_results: List[DictAnalyzerResult], entities: List[str]
    ) -> Dict[str, List[Any]]:
        anonymizer_results = self._batch_anonymizer.anonymize_dict(
            analyzer_results,
            operators={
                "EMAIL_ADDRESS": OperatorConfig("custom", {"lambda": fake_email}),
            },
        )
        return anonymizer_results

    def _log_aggregate_results(self, analyzer_results: List[DictAnalyzerResult]):
        for result in analyzer_results:
            column_name = result.key
            entities_counter_map = defaultdict(int)

            for recognizer_result in result.recognizer_results:
                if len(recognizer_result) > 0:
                    entities_counter_map[recognizer_result[0].entity_type] += 1

            if len(entities_counter_map) > 0:
                logger.info(
                    f"[{column_name}] contains the following entities: {dict(entities_counter_map)}."
                )

    def _new_file_name(self, path: str) -> str:
        return path.split(".")[0] + "_scrubbed." + path.split(".")[1]
