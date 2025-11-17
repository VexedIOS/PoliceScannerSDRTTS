import os
from AnyTextToSpeech.AnyTextToSpeechBuilder import AnyTextToSpeechBuild
from AnyTextToSpeech.SplitterModels.TextToSpeechSplitter import TextToSpeechSplitter
from AnyTextToSpeech.TextToSpeechModels.WhisperTextToSpeechSmallEn import WhisperTextToSpeechSmallEn
from AnyTextToSpeech.folder_utils import check_all_files_in_folder
import sqlite3

class SDRTrunkLogger:
    DEFAULT_LOGFILE_NAME= "log.db"

    def __init__(self, recording_file_path, output_file_path, log_=True, save_recordings=False):
        self.recording_file_path = recording_file_path
        self.output_file_path = output_file_path
        self.log_ = log_
        self.save_recordings = save_recordings
        self.used_files = set()
        if self.log_:
            self.logger_path = os.path.abspath(f"{self.output_file_path}/{SDRTrunkLogger.DEFAULT_LOGFILE_NAME}")
            if os.path.exists(self.logger_path):
                print("Log File Exists")
                self.used_files = self.grab_used_files()
            else:
                self.create_database()

    def run(self):
        while True:
            self.used_files = self.grab_used_files()
            list_files = check_all_files_in_folder(starting_file_dir := self.recording_file_path,)
            oldest_first_ordered = sorted(list_files,
                                          key=lambda f: os.path.getmtime(os.path.join(starting_file_dir, f)))

            oldest_first_ordered = [file_name for file_name in oldest_first_ordered if file_name not in self.used_files]
            if oldest_first_ordered:
                for file_name in oldest_first_ordered:
                    self.used_files.add(file_name)
                    any_tts = AnyTextToSpeechBuild(splitter=TextToSpeechSplitter,
                                                   texttospeech=WhisperTextToSpeechSmallEn,
                                                   raw_audio_path=file_name,
                                                   output_path=self.output_file_path)
                    any_tts.text_to_speech()
                    clean_text = any_tts.clean_SDR_text()
                    info_ = any_tts.SDR_INFO()
                    info_.append(file_name)
                    print(clean_text)
                    self.update_database(info_)
                    if not self.save_recordings:
                        any_tts.delete_all_files()
                    if self.log_:
                        self.update_database(info_)

    def create_database(self):
        conn = sqlite3.connect(self.logger_path)
        cursor = conn.cursor()
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS logs(
            timestamp TEXT NOT NULL,
            talkgroup TEXT,
            text TEXT,
            filename TEXT UNIQUE
            );  
        """
        cursor.execute(create_table_sql)
        print("Table 'logs' created successfully.")
        conn.commit()
        cursor.close()
        conn.close()

    def grab_used_files(self):
        conn = sqlite3.connect(self.logger_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT filename FROM logs")
        conn.commit()
        row_set = {row[0] for row in cursor.fetchall()}
        cursor.close()
        conn.close()
        return row_set

    def update_database(self, info):
        try:
            conn = sqlite3.connect(self.logger_path)
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO logs (timestamp, talkgroup, text, filename) VALUES (?, ?, ?, ?)", info)
            conn.commit()
            cursor.close()
            conn.close()
        except sqlite3.IntegrityError or sqlite3.OperationalError:
            cursor.close()
            conn.close()





logger = SDRTrunkLogger(recording_file_path="/home/vexed/SDRTrunk/recordings/",
               output_file_path="/home/vexed/PycharmProjects/PoliceScannerSDR/data/processed",
                        log_=True,
                        save_recordings=False)
logger.run()