import xml.sax
import multiprocessing
import sqlite3
from concurrent.futures import ProcessPoolExecutor
import time

class SEPAHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.current_tag = ""
        self.current_data = ""
        self.instruction = {}
        self.instructions = []

    def startElement(self, tag, attributes):
        self.current_tag = tag

    def characters(self, content):
        self.current_data = content.strip()

    def endElement(self, tag):
        if tag == "DrctDbtTxInf":
            self.instructions.append(self.instruction)
            self.instruction = {}
        elif tag in ["EndToEndId", "InstdAmt", "IBAN"]:
            self.instruction[tag] = self.current_data

def process_chunk(chunk):
    start_time = time.time()
    parser = xml.sax.make_parser()
    handler = SEPAHandler()
    parser.setContentHandler(handler)
    parser.parse(chunk)
    end_time = time.time()
    processing_time = end_time - start_time
    return handler.instructions, processing_time

def insert_instructions(db_name, instructions):
    start_time = time.time()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO instructions (end_to_end_id, amount, iban)
        VALUES (:EndToEndId, :InstdAmt, :IBAN)
    ''', instructions)
    conn.commit()
    conn.close()
    end_time = time.time()
    insertion_time = end_time - start_time
    return insertion_time

def main():
    overall_start_time = time.time()

    db_name = 'sepa_instructions.db'
    
    # Create SQLite database and table
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS instructions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            end_to_end_id TEXT,
            amount TEXT,
            iban TEXT
        )
    ''')
    conn.commit()
    conn.close()

    # Divide file into chunks (this is a simplified example)
    chunk_size = 1000000  # Adjust based on your system's capabilities
    chunks = ['sample_sepa_sdd.xml']  # Assume single file for simplicity

    # Process chunks in parallel
    processing_start_time = time.time()
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_chunk, chunks))
    processing_end_time = time.time()
    total_processing_time = processing_end_time - processing_start_time

    # Insert results into SQLite database
    total_insertion_time = 0
    for chunk_result, chunk_processing_time in results:
        insertion_time = insert_instructions(db_name, chunk_result)
        total_insertion_time += insertion_time
        print(f"Chunk processed in {chunk_processing_time:.2f} seconds, inserted in {insertion_time:.2f} seconds")

    overall_end_time = time.time()
    overall_execution_time = overall_end_time - overall_start_time

    print(f"Total processing time: {total_processing_time:.2f} seconds")
    print(f"Total database insertion time: {total_insertion_time:.2f} seconds")
    print(f"Overall execution time: {overall_execution_time:.2f} seconds")

if __name__ == "__main__":
    main()