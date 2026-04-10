#!/usr/bin/env python3
"""
Concatenate transcripts by request_id (or id) with speaker labels.

Defaults:
 - input: xlsx_csv_files/cred_20_set_2.xlsx (auto-detect CSV/XLSX)
 - output: xlsx_csv_files/concatenated_by_request.csv

Speaker mapping:
 - 0 -> Agent
 - 1 -> Customer

Produces a CSV with columns: id, transcript
"""

import argparse
from pathlib import Path
import pandas as pd
import sys

def find_column(cols, candidates):
    lc = {c.lower().strip(): c for c in cols}
    for cand in candidates:
        key = cand.lower().strip()
        if key in lc:
            return lc[key]
    return None

def map_speaker_value(val):
    # Map numeric 0/1 to Agent/Customer; if already Agent/Customer-like, normalize
    if pd.isna(val):
        return 'Unknown'
    try:
        if isinstance(val, (int, float)):
            if int(val) == 0:
                return 'Agent'
            if int(val) == 1:
                return 'Customer'
        s = str(val).strip()
        if s in {'0', '1'}:
            return 'Agent' if s == '0' else 'Customer'
        # common labels
        low = s.lower()
        if 'agent' in low or 'executive' in low or 'rep' in low or 'caller' in low:
            return 'Agent'
        if 'customer' in low or 'user' in low or 'client' in low or 'caller' in low:
            return 'Customer'
        # fallback: unknown
        return s.capitalize()
    except Exception:
        return str(val)

def concatenate(input_path: Path, output_path: Path, sheet_name: str = None, sep: str = ' '):
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Read file (CSV or Excel)
    if input_path.suffix.lower() in ['.csv']:
        df = pd.read_csv(input_path)
    else:
        xl = pd.ExcelFile(input_path)
        sheet = sheet_name if sheet_name and sheet_name in xl.sheet_names else xl.sheet_names[0]
        df = pd.read_excel(input_path, sheet_name=sheet)

    # Normalize column names
    df.columns = [c.strip() for c in df.columns]

    # Detect columns
    id_col = find_column(df.columns, ['request_id', 'conversation_id', 'id', 'request id'])
    transcript_col = find_column(df.columns, ['transcript', 'transcripts', 'text', 'utterance'])
    speaker_col = find_column(df.columns, ['speaker', 'speaker_id', 'speaker_label', 'role'])
    time_col = find_column(df.columns, ['starttime', 'start_time', 'timestamp', 'time', 'start'])

    # If the file already contains grouped transcripts (id + transcripts), just normalize and write out
    if id_col is not None and transcript_col is not None and speaker_col is None:
        out_df = df[[id_col, transcript_col]].copy()
        out_df.columns = ['id', 'transcript']
        out_df.to_csv(output_path, index=False, sep='\t')
        print(f"ℹ️ Input appears pre-grouped. Written {len(out_df)} conversations to {output_path}")
        return out_df

    if id_col is None or transcript_col is None or speaker_col is None:
        raise ValueError(f"Required columns not found. Found columns: {list(df.columns)}")

    # Ensure start time exists for ordering; if not, create ordinal index per group
    if time_col is None:
        df['_order'] = df.groupby(id_col).cumcount()
        order_col = '_order'
    else:
        # coerce to numeric where possible
        try:
            df[time_col] = pd.to_numeric(df[time_col], errors='coerce')
        except Exception:
            pass
        order_col = time_col

    # Fill NaN transcript as empty
    df[transcript_col] = df[transcript_col].fillna('').astype(str)

    # Map speaker values
    df['_speaker_label'] = df[speaker_col].apply(map_speaker_value)

    # Build combined text per row
    df['_combined'] = df['_speaker_label'].str.strip() + ': ' + df[transcript_col].str.strip()

    # Sort and group
    df_sorted = df.sort_values(by=[id_col, order_col])

    grouped = df_sorted.groupby(id_col)['_combined'].apply(lambda xs: sep.join([x for x in xs if x and x.strip()]))

    out_df = grouped.reset_index()
    out_df.columns = ['id', 'transcript']

    # Save CSV
    out_df.to_csv(output_path, index=False, sep='\t')

    print(f"✅ Written {len(out_df)} conversations to {output_path}")

    return out_df


def main():
    parser = argparse.ArgumentParser(description='Concatenate transcripts by request_id with speaker labels')
    parser.add_argument('--input', '-i', type=str, default='xlsx_csv_files/cred_20_set_2.xlsx')
    parser.add_argument('--output', '-o', type=str, default='xlsx_csv_files/concatenated_by_request.tsv')
    parser.add_argument('--sheet', type=str, default=None)
    parser.add_argument('--sep', type=str, default=' ')
    args = parser.parse_args()

    inp = Path(args.input)
    out = Path(args.output)
    concatenate(inp, out, sheet_name=args.sheet, sep=args.sep)


if __name__ == '__main__':
    main()
