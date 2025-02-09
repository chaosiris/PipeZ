import os
import sys
import ffmpeg

def change_sample_rate(file_path, output_path, target_sample_rate):
    ffmpeg.input(file_path).output(output_path, ar=target_sample_rate).global_args('-loglevel', 'error').run()
    
def copy_metadata_file(src, dest):
    with open(src, 'rb') as f_src:
        with open(dest, 'wb') as f_dest:
            f_dest.write(f_src.read())
    print("Copied metadata.csv to 'final' folder")

def check_metadata_files(final_folder, metadata_file):
    missing_files = []
    with open(metadata_file, 'r') as f:
        for line in f:
            filename = line.strip().split('|')[0] + '.wav'
            if not os.path.exists(os.path.join(final_folder, filename)):
                missing_files.append(filename)
    if missing_files:
        print("The following files listed in metadata.csv were not found in the 'final' folder. Please restart the process or fix/remove the affected files.")
        for file in missing_files:
            print(file)
    else:
        print("All files listed in metadata.csv are present in the 'final' folder")

def unify_sample_rates(target_sample_rate):
    print(f"Starting automatic process of unifying all audio samples to {target_sample_rate} Hz based on chosen checkpoint file...")
    training_folder = os.path.join(os.getcwd(), 'training_data')
    final_folder = os.path.join(training_folder, 'final')
    metadata_file = os.path.join(training_folder, 'metadata.csv')

    if not os.path.exists(final_folder):
        os.makedirs(final_folder)

    for root, dirs, files in os.walk(training_folder):
        if 'final' in dirs:
            dirs.remove('final')
        if 'backup' in dirs:
            dirs.remove('backup')
        for file in files:
            if file.endswith('.wav'):
                file_path = os.path.join(root, file)
                output_path = os.path.join(final_folder, file)
                change_sample_rate(file_path, output_path, target_sample_rate)
                print(f"Converted {file} to {target_sample_rate} Hz sample rate and moved to 'final' folder")

    if os.path.exists(metadata_file):
        copy_metadata_file(metadata_file, os.path.join(final_folder, 'metadata.csv'))
        check_metadata_files(final_folder, os.path.join(final_folder, 'metadata.csv'))

    print("Preprocessing has been successfully completed!")

def main():
    if len(sys.argv) != 2:
        print("Usage: python unify_sample_rate.py <sample_rate>")
        sys.exit(1)

    target_sample_rate = int(sys.argv[1])
    unify_sample_rates(target_sample_rate)
    print("Please proceed to run 5_convert_data.bat to convert the preprocessed data into Piper's ljspeech format (used for training)!")
    sys.exit(0)

if __name__ == "__main__":
    main()
