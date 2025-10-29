import pandas as pd
from tqdm import tqdm
from tasks.compilation.single_compilation import get_prediction_for_question


INPUT_CSV = "./vendor/design_qa/dataset/rule_extraction/rule_compilation_qa.csv"
OUTPUT_CSV = "./data/outputs/compilation_predictions.csv"


def main():
    df = pd.read_csv(INPUT_CSV)
    model_predictions = []

    for _, row in tqdm(df.iterrows(), total=len(df)):
        question = row["question"]
        model_predictions.append(get_prediction_for_question(question))

    df["model_prediction"] = model_predictions
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")


if __name__ == "__main__":
    main()
