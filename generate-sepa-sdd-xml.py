import random
from datetime import datetime, timedelta
import time

def generate_sample_xml(num_instructions, filename):
    start_time = time.time()
    
    with open(filename, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.008.001.02">\n')
        f.write('  <CstmrDrctDbtInitn>\n')
        f.write('    <GrpHdr>\n')
        f.write('      <MsgId>MSG-' + datetime.now().strftime('%Y%m%d%H%M%S') + '</MsgId>\n')
        f.write('      <CreDtTm>' + datetime.now().isoformat() + '</CreDtTm>\n')
        f.write('      <NbOfTxs>' + str(num_instructions) + '</NbOfTxs>\n')
        f.write('    </GrpHdr>\n')
        f.write('    <PmtInf>\n')

        for i in range(num_instructions):
            end_to_end_id = f'E2E-{i:08d}'
            amount = round(random.uniform(10, 10000), 2)
            iban = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=22))
            
            f.write('      <DrctDbtTxInf>\n')
            f.write(f'        <PmtId>\n')
            f.write(f'          <EndToEndId>{end_to_end_id}</EndToEndId>\n')
            f.write(f'        </PmtId>\n')
            f.write(f'        <InstdAmt Ccy="EUR">{amount:.2f}</InstdAmt>\n')
            f.write(f'        <DbtrAcct>\n')
            f.write(f'          <Id>\n')
            f.write(f'            <IBAN>{iban}</IBAN>\n')
            f.write(f'          </Id>\n')
            f.write(f'        </DbtrAcct>\n')
            f.write('      </DrctDbtTxInf>\n')

            if i % 100000 == 0:
                print(f'Generated {i} instructions')

        f.write('    </PmtInf>\n')
        f.write('  </CstmrDrctDbtInitn>\n')
        f.write('</Document>\n')

    end_time = time.time()
    execution_time = end_time - start_time
    print(f'Generated {num_instructions} instructions in {filename}')
    print(f'File generation took {execution_time:.2f} seconds')

# Usage
generate_sample_xml(2000000, 'sample_sepa_sdd.xml')