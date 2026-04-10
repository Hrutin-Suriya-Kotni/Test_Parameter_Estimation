import pandas as pd

def generate_concatenated_transcripts():
    # File paths
    input_file = "/media/vocab/ab36a93d-73ed-432d-98d0-e1e6926ff4253/kashyap/Test_Parameter_Estimation/xlsx_csv_files/Lenovo 20 new calls - to generate output from Surya 2&3.xlsx"
    output_file = "/home/vocab/25_gcp_testing/audios/lenova_20_set_2.xlsx"

    # Load Excel file
    df = pd.read_excel(input_file)

    # Normalize column names (strip and keep original names mapping)
    df.columns = df.columns.str.strip()
    cols_lc = {c.lower(): c for c in df.columns}

    # Heuristics for column names (fall back to common alternatives)
    def find_col(candidates):
        for cand in candidates:
            if cand in cols_lc:
                return cols_lc[cand]
        return None

    conv_col = find_col(["conversation_id", "conversation id", "id", "request_id", "request id"])
    transcript_col = find_col(["transcript", "transcripts", "text", "utterance"])
    speaker_col = find_col(["speaker", "role", "speaker_label", "speaker name"])
    start_col = find_col(["starttime", "start_time", "timestamp", "time", "start"])

    missing = []
    if conv_col is None:
        missing.append("conversation_id (or id/request_id)")
    if transcript_col is None:
        missing.append("transcript")
    if speaker_col is None:
        missing.append("speaker")
    if start_col is None:
        missing.append("starttime (start_time/timestamp)")

    if missing:
        raise ValueError(f"Missing column(s): {', '.join(missing)}. Found columns: {list(df.columns)}")

    # Convert starttime to numeric (for proper sorting)
    df[start_col] = pd.to_numeric(df[start_col], errors="coerce")

    # Sort by conversation and time
    df = df.sort_values(by=[conv_col, start_col])

    # Clean transcript column
    df[transcript_col] = df[transcript_col].fillna("").astype(str)

    # Remove empty transcripts
    df = df[df[transcript_col].str.strip() != ""]

    # Format speaker labels
    df[speaker_col] = df[speaker_col].fillna("unknown").astype(str).str.capitalize()

    # Combine speaker + transcript
    df["combined"] = df[speaker_col] + ": " + df[transcript_col]

    # Group and concatenate
    final_df = df.groupby(conv_col)["combined"].apply(
        lambda x: "\n".join(x)
    ).reset_index()

    # Rename columns
    final_df.columns = ["id", "transcripts"]

    # Save to Excel
    final_df.to_excel(output_file, index=False)

    print(f"✅ Output saved to: {output_file}")


if __name__ == "__main__":
    generate_concatenated_transcripts()