import csv
import os

def log_image_to_csv(prompt, caption, url, csv_path='image_log.csv'):
    file_exists = os.path.isfile(csv_path)
    
    with open(csv_path, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['ImagePrompt', 'ImageCaption', 'ImageURL'])

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'ImagePrompt': prompt,
            'ImageCaption': caption,
            'ImageURL': url
        })