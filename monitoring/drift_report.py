import pandas as pd
try:
    from evidently.report import Report
    from evidently.metric_preset import DataDriftPreset
except ImportError:
    print("Evidently not installed. Please install 'evidently' to run this script.")
    exit(1)

def generate_drift_report(reference_path, current_path, output_path="drift_report.html"):
    print("Loading data for drift analysis...")
    reference = pd.read_parquet(reference_path)
    current = pd.read_parquet(current_path)
    
    print("Running Evidently drift report...")
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference, current_data=current)
    
    report.save_html(output_path)
    print(f"Drift report saved to {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--ref", required=True, help="Path to reference data (parquet)")
    parser.add_argument("--curr", required=True, help="Path to current data (parquet)")
    parser.add_argument("--out", default="drift_report.html", help="Output HTML path")
    args = parser.parse_args()

    generate_drift_report(args.ref, args.curr, args.out)

