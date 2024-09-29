from typing import  Optional
import re
from petl.util.base import DictsView
from os import path
from datetime import datetime
from dataclasses import dataclass
from typing import Iterable, Mapping

from beangulp_importers.string_utils import match_filepath_date, match_filepath_extension, match_filepath_pattern, extract_date_from_filename
from beangulp_importers.file_utils import match_csv_header, match_csv_entry, match_xlsx_header, match_xlsx_entry, read_csv_table, read_xlsx_table
   

@dataclass(kw_only=True, frozen=True)
class FileDescriptionCSV:
    """
    A class to identify files based on specific criteria such as 
    file extension, name pattern, and date. In addition the file content iteself is also analysed

    Attributes:
        file_extension (str): The expected file extension (default is .csv).
        file_pattern_regex (str): The regular expression pattern for filename matching.
        file_date_format (str): The format for parsing dates from filenames (default is "%Y-%m-%d").
        file_header (Iterable[str]): The file header description for matching to the file.
        entry_mapping (Mapping[str, str]): A mapping with the element key and its desired value for matching.
        start_date (Optional[datetime.date]): An optional start date for date validation.
        end_date (Optional[datetime.date]): An optional end date for date validation.
    """
    file_extension: str = '.csv'
    file_pattern_regex: str
    file_date_format: str = "%Y-%m-%d"
    file_header: Iterable[str]
    entry_mapping: Optional[Mapping[str, str]] = None
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None


    def identify(self, filepath: str) -> bool:
        """
        Identify if the file matches the specified criteria.

        This method checks the file extension, filename pattern, and file date.

        Args:
            filepath (str): The path to the file to be identified.

        Returns:
            bool: True if the file matches all criteria; False otherwise.

        Raises:
            ValueError: If the filepath is empty or if an error occurs during validation.
        """
        # Identification of only the file name
        if not filepath:
            raise ValueError("The provided filepath is empty.")

        if not match_filepath_extension(filepath, self.file_extension):
            return False
        
        if not match_filepath_pattern(filepath, self.file_pattern_regex):
            return False
        
        if not match_filepath_date(filepath, self.file_pattern_regex, self.file_date_format, self.start_date, self.end_date):
            return False
        
        # Starting deep identification by reading the actual file
        if not match_csv_header(filepath, self.file_header):
            return False
        
        if self.entry_mapping and not match_csv_entry(filepath, self.entry_mapping):
            return False
        
        return True
    
    def date(self, filepath: str) -> datetime.date:
        """
        Extract the date from the filename in the specified file path using the configured regex pattern.

        Parameters:
            filepath (str): The file path from which to extract the date.

        Returns:
            datetime.date: The extracted date from the filename.

        Raises:
            ValueError: If the date cannot be extracted or parsed from the filename.
        """
        return extract_date_from_filename(filepath, self.file_pattern_regex, self.file_date_format)
    
    def name(self, filepath: str) -> str:
        return filepath.replace(' ', '_')
    
    def read(self, filepath: str) -> DictsView:
        return read_csv_table(filepath)


@dataclass(kw_only=True, frozen=True)
class FileDescriptionXLSX:
    """
    A class to identify files based on specific criteria such as 
    file extension, name pattern, and date. In addition the file content iteself is also analysed

    Attributes:
        file_extension (str): The expected file extension (default is .xlsx).
        file_pattern_regex (str): The regular expression pattern for filename matching.
        file_date_format (str): The format for parsing dates from filenames (default is "%Y-%m-%d").
        file_header (Iterable[str]): The file header description for matching to the file.
        entry_mapping (Mapping[str, str]): A mapping with the element key and its desired value for matching.
        start_date (Optional[datetime.date]): An optional start date for date validation.
        end_date (Optional[datetime.date]): An optional end date for date validation.
    """
    file_extension: str = '.xlsx'
    file_pattern_regex: str
    file_date_format: str = "%Y-%m-%d"
    file_header: Iterable[str]
    entry_mapping: Optional[Mapping[str, str]] = None
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None


    def identify(self, filepath: str) -> bool:
        """
        Identify if the file matches the specified criteria.

        This method checks the file extension, filename pattern, and file date.

        Args:
            filepath (str): The path to the file to be identified.

        Returns:
            bool: True if the file matches all criteria; False otherwise.

        Raises:
            ValueError: If the filepath is empty or if an error occurs during validation.
        """
        # Identification of only the file name
        if not filepath:
            raise ValueError("The provided filepath is empty.")

        if not match_filepath_extension(filepath, self.file_extension):
            return False
        
        if not match_filepath_pattern(filepath, self.file_pattern_regex):
            return False
        
        if not match_filepath_date(filepath, self.file_pattern_regex, self.file_date_format, self.start_date, self.end_date):
            return False
        
        # Starting deep identification by reading the actual file
        if not match_xlsx_header(filepath, self.file_header):
            return False
        
        if self.entry_mapping and not match_xlsx_entry(filepath, self.entry_mapping):
            return False
        
        return True
    
    def date(self, filepath: str) -> datetime.date:
        """
        Extract the date from the filename in the specified file path using the configured regex pattern.

        Parameters:
            filepath (str): The file path from which to extract the date.

        Returns:
            datetime.date: The extracted date from the filename.

        Raises:
            ValueError: If the date cannot be extracted or parsed from the filename.
        """
        return extract_date_from_filename(filepath, self.file_pattern_regex, self.file_date_format)
    
    def name(self, filepath: str) -> str:
        return filepath.replace(' ', '_')
    
    def read(self, filepath: str) -> DictsView:
        return read_xlsx_table(filepath)