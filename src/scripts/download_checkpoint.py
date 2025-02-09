import os
import requests

def download_checkpoint(url, language, gender, speaker, quality, folder, rename):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    if rename:
        file_extension = url.split('.')[-1].split('?')[0]
        new_filename = f"{language}_{gender}_{speaker}_{quality}.{file_extension}"
    else:
        new_filename = url.split('/')[-1].split('?')[0]
    
    output_path = os.path.join(folder, new_filename)
    
    with open(output_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"Downloaded and saved {output_path}")
    
    return new_filename if rename else None

def save_settings(language, quality, checkpoint_filename=None):
    sample_rate = 16000 if quality == 'low' else 22050
    with open('SETTINGS.txt', 'w') as f:
        f.write(f"ESPEAK_LANGUAGE_CODE={language}\n")
        f.write(f"CHECKPOINT_SAMPLE_RATE={sample_rate}\n")
        if checkpoint_filename:
            f.write(f"CHECKPOINT_FILE={checkpoint_filename}\n")

def main():
    # Create checkpoint folder if it doesn't exist
    if not os.path.exists("downloaded_checkpoint"):
        os.makedirs("downloaded_checkpoint")

    download_folder = os.path.join(os.getcwd(), "downloaded_checkpoint")

    # Check if a checkpoint file already exists
    existing_checkpoints = [f for f in os.listdir(download_folder) if f.endswith('.ckpt')]
    if existing_checkpoints:
        print("Existing checkpoint files found:")
        for checkpoint in existing_checkpoints:
            print(f"{checkpoint}")
        delete_existing = input("Do you want to delete the existing checkpoint files before downloading new ones? (yes/no): ").strip().lower()
        if delete_existing == "yes":
            for checkpoint in existing_checkpoints:
                os.remove(os.path.join(download_folder, checkpoint))
            print("Deleted existing checkpoint files.")
        else:
            print("Please delete the existing checkpoint files before downloading new ones.")
            return

    languages = {
        "en-us": "English (United States)",
        "en": "English (United Kingdom)",
        "fr": "French",
        "es": "Spanish",
        "de": "German",
        "cn": "Mandarin Chinese"
    }

    links = {
        "en-us": {
            "male": {
                "bryce": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/bryce/medium/bryce-3499.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/bryce/medium/config.json?download=true"
                    },
                },
                "arctic": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/arctic/medium/epoch%3D663-step%3D646736.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/arctic/medium/config.json?download=true"
                    },
                },
                "hfc_male": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/hfc_male/medium/epoch%3D2785-step%3D2128064.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/hfc_male/medium/config.json?download=true"
                    },
                },
                "joe": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/joe/medium/epoch%3D7889-step%3D1221224.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/joe/medium/config.json?download=true"
                    },
                },
                "john": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/john/medium/john-2599.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/john/medium/config.json?download=true"
                    },
                },
                "kusal": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/kusal/medium/epoch%3D2652-step%3D1953828.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/kusal/medium/config.json?download=true"
                    },
                },
                "l2arctic": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/l2arctic/medium/epoch%3D536-step%3D902160.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/l2arctic/medium/config.json?download=true"
                    },
                },
                "kusal": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/kusal/medium/epoch%3D2652-step%3D1953828.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/kusal/medium/config.json?download=true"
                    },
                },
                "ryan": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/ryan/medium/epoch%3D4641-step%3D3104302.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/ryan/medium/config.json?download=true"
                    },
                },
            },
            "female": {
                "amy": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/amy/medium/epoch%3D6679-step%3D1554200.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/amy/medium/config.json?download=true"
                    },
                },
                "hfc_female": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/hfc_female/medium/epoch%3D2868-step%3D1575188.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/hfc_female/medium/config.json?download=true"
                    },
                },
                "kristin": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/kristin/medium/kristin-2000.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/kristin/medium/config.json?download=true"
                    },
                },
                "lessac": {
                    "low": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/lessac/low/epoch%3D2307-step%3D558536.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/lessac/low/config.json?download=true"
                    },
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/lessac/medium/epoch%3D2164-step%3D1355540.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/lessac/medium/config.json?download=true"
                    },
                    "high": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/lessac/high/epoch%3D2218-step%3D838782.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/lessac/high/config.json?download=true"
                    },
                },
                "libritts_r": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/libritts_r/medium/epoch%3D404-step%3D1887300.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/libritts_r/medium/config.json?download=true"
                    },
                },
                "ljspeech": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/ljspeech/medium/lj-med_1000.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/ljspeech/medium/config.json?download=true"
                    },
                    "high": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/ljspeech/high/ljspeech-2000.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/ljspeech/high/config.json?download=true"
                    },
                },
            }
        },
        "en": {
            "male": {
                "alan": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_GB/alan/medium/epoch%3D6339-step%3D1647790.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_GB/alan/medium/config.json?download=true"
                    },
                },
                "northern_english_male": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_GB/northern_english_male/medium/epoch%3D9029-step%3D2261720.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_GB/northern_english_male/medium/config.json?download=true"
                    },
                },
                "hfc_male": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/hfc_male/medium/epoch%3D2785-step%3D2128064.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/hfc_male/medium/config.json?download=true"
                    },
                },
                "joe": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/joe/medium/epoch%3D7889-step%3D1221224.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/joe/medium/config.json?download=true"
                    },
                },
                "john": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/john/medium/john-2599.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/john/medium/config.json?download=true"
                    },
                },
                "kusal": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/kusal/medium/epoch%3D2652-step%3D1953828.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/kusal/medium/config.json?download=true"
                    },
                },
                "l2arctic": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/l2arctic/medium/epoch%3D536-step%3D902160.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/l2arctic/medium/config.json?download=true"
                    },
                },
                "kusal": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/kusal/medium/epoch%3D2652-step%3D1953828.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/kusal/medium/config.json?download=true"
                    },
                },
                "ryan": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/ryan/medium/epoch%3D4641-step%3D3104302.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_US/ryan/medium/config.json?download=true"
                    },
                },
            },
            "female": {
                "alba": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_GB/alba/medium/epoch%3D4179-step%3D2101090.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_GB/alba/medium/config.json?download=true"
                    },
                },
                "aru": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_GB/aru/medium/epoch%3D3479-step%3D939600.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_GB/aru/medium/config.json?download=true"
                    },
                },
                "cori": {
                    "high": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_GB/cori/high/cori-high-500.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_GB/cori/high/config.json?download=true"
                    },
                },
                "jenny_dioco": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_GB/jenny_dioco/medium/epoch%3D2748-step%3D1729300.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_GB/jenny_dioco/medium/config.json?download=true"
                    },
                },
                "semaine": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_GB/semaine/medium/epoch%3D1849-step%3D214600.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_GB/semaine/medium/config.json?download=true"
                    },
                },
                "vctk": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_GB/vctk/medium/epoch%3D545-step%3D1511328.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/en/en_GB/vctk/medium/config.json?download=true"
                    },
                },
            }
        },
        "fr": {
            "male": {
                "mls": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/fr/fr_FR/mls/medium/epoch%3D317-step%3D3124032.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/fr/fr_FR/mls/medium/config.json?download=true"
                    },
                }
            },
            "female": {
                "siwis": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/fr/fr_FR/siwis/medium/epoch%3D3304-step%3D2050940.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/fr/fr_FR/siwis/medium/config.json?download=true"
                    },
                },
                "upmc": {
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/fr/fr_FR/upmc/medium/epoch%3D2999-step%3D702000.ckpt?download=true",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/fr/fr_FR/upmc/medium/config.json?download=true"
                    },
                },
            }
        },
        "es": {
            "female": {
                "carmen": {
                    "low": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/es/es_ES/carmen/low/checkpoint.ckpt",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/es/es_ES/carmen/low/config.json"
                    },
                    "medium": {
                        "checkpoint": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/es/es_ES/carmen/medium/checkpoint.ckpt",
                        "config": "https://huggingface.co/datasets/rhasspy/piper-checkpoints/es/es_ES/carmen/medium/config.json"
                    }
                }
            }
        },
    }

    print("Available languages:")
    for code, language in languages.items():
        print(f"{code}: {language}")

    selected_language = input("Enter the language code that you wish to train: ").strip().lower()
    if selected_language not in languages:
        print("Invalid language code. Exiting.")
        return

    print("Available genders for: " + selected_language)
    genders = links.get(selected_language, {})
    for gender in genders.keys():
        print(f"{gender.capitalize()}")

    selected_gender = input("Enter the gender (male/female): ").strip().lower()
    if selected_gender not in genders:
        print("Invalid gender. Exiting.")
        return

    available_speakers = links[selected_language].get(selected_gender, {})
    if not available_speakers:
        print(f"No available speakers for the selected language '{languages[selected_language]}' and gender '{selected_gender}'. Exiting.")
        return

    print("Available speakers:")
    for code in available_speakers.keys():
        print(f"{code}")

    selected_speaker = input("Enter the speaker code: ").strip().lower()
    if selected_speaker not in available_speakers:
        print("Invalid speaker code. Exiting.")
        return

    available_qualities = available_speakers.get(selected_speaker, {})
    if not available_qualities:
        print(f"No available qualities for the selected speaker '{selected_speaker}'. Exiting.")
        return

    print("Available quality options:")
    for code in available_qualities.keys():
        print(f"{code}: {code.capitalize()}")

    selected_quality = input("Enter the quality code: ").strip().lower()
    if selected_quality not in available_qualities:
        print("Invalid quality code. Exiting.")
        return

    try:
        checkpoint_url = available_qualities[selected_quality]["checkpoint"]
        config_url = available_qualities[selected_quality]["config"]

        print(f"Downloading checkpoint file from {checkpoint_url}...")
        checkpoint_filename = download_checkpoint(checkpoint_url, selected_language, selected_gender, selected_speaker, selected_quality, download_folder, True)
        
        print(f"Downloading config file from {config_url}...")
        download_checkpoint(config_url, selected_language, selected_gender, selected_speaker, selected_quality, download_folder, False)

        save_settings(selected_language, selected_quality, checkpoint_filename)

        print("Download completed.")
    except KeyError:
        print("Link for the selected language, gender, speaker, and quality combination is not available. Exiting.")

if __name__ == "__main__":
    print("Please select a checkpoint file to download. The voice of the checkpoint file should resemble your audio files/training data as closely as possible.")
    print("You can test each checkpoint file to gauge its similarity @ https://rhasspy.github.io/piper-samples/")
    main()
