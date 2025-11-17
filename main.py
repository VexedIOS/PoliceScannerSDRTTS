from AnyTextToSpeech.ContinousFileChecker import SDRTrunkLogger

if __name__ == "__main__":
    # This code will only run when the script is executed directly
    logger = SDRTrunkLogger(recording_file_path="/home/vexed/SDRTrunk/recordings/",
                            output_file_path="/home/vexed/PycharmProjects/PoliceScannerSDR/data/processed",
                            log_=True,
                            save_recordings=False)
    logger.run()