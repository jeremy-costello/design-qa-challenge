import pandas as pd
from tqdm import tqdm
from tasks.retrieval.single_retrieval import get_prediction_for_question


INPUT_CSV_FILE = "./vendor/design_qa/dataset/rule_extraction/rule_retrieval_qa.csv"
OUTPUT_CSV_FILE = "./data/outputs/retrieval_predictions.csv"


def main():
    df = pd.read_csv(INPUT_CSV_FILE)
    model_predictions = []

    for _, row in tqdm(df.iterrows(), total=len(df)):
        question = row["question"]
        model_predictions.append(get_prediction_for_question(question))

    df["model_prediction"] = model_predictions
    df.to_csv(OUTPUT_CSV_FILE, index=False, encoding="utf-8")


if __name__ == "__main__":
    main()
