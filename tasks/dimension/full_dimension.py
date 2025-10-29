import pandas as pd
from tqdm import tqdm
from tasks.dimension.single_dimension import get_prediction_for_question


INPUT_CSV = "./vendor/design_qa/dataset/rule_compliance/rule_dimension_qa/context/rule_dimension_qa_context.csv"
OUTPUT_CSV = "./data/outputs/dimension_predictions.csv"


def main():
    df = pd.read_csv(INPUT_CSV)
    model_predictions = []

    for _, row in tqdm(df.iterrows(), total=len(df)):
        question = row["question"]
        image_name = row["image"]
        prediction = get_prediction_for_question(
            question=question,
            image_name=image_name
        )
        model_predictions.append(prediction)

    df["model_prediction"] = model_predictions
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")


if __name__ == "__main__":
    main()
