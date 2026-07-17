import pandas as pd
import os
import joblib
from sklearn.preprocessing import OneHotEncoder


# Project root directory
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

ENCODER_PATH = os.path.join(
    MODEL_DIR,
    "encoder.pkl"
)



def preprocess_data(df, training=True, target_column=None):

    print("\n========== PREPROCESSING STARTED ==========")


    # avoid modifying original dataframe
    df = df.copy()


    target = None


    # ---------------------------------
    # 0. Separate target column
    # ---------------------------------

    if target_column and target_column in df.columns:
        target = df[target_column]



    # ---------------------------------
    # 1. Remove duplicate rows
    # ---------------------------------

    duplicates = df.duplicated().sum()


    if duplicates > 0:

        print(
            f"Removing {duplicates} duplicate rows"
        )

        df = df.drop_duplicates()


        if target is not None:

            target = target.loc[df.index]


    else:

        print(
            "No duplicate rows found"
        )



    # ---------------------------------
    # 2. Remove useless columns
    # ---------------------------------

    useless_columns = [
        "customerID",
        "CustomerID",
        "customer_id",
        "id"
    ]


    removed=[]


    for col in useless_columns:

        if col in df.columns:

            df.drop(
                col,
                axis=1,
                inplace=True
            )

            removed.append(col)



    if removed:

        print(
            "Removed:",
            removed
        )

    else:

        print(
            "No useless columns found"
        )



    # ---------------------------------
    # 3. Convert only known numeric columns
    # ---------------------------------

    numeric_columns = [
        "SeniorCitizen",
        "tenure",
        "MonthlyCharges",
        "TotalCharges"
    ]


    for col in numeric_columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )



    # ---------------------------------
    # 4. Handle missing values
    # ---------------------------------

    missing = df.isnull().sum()


    if missing.sum() > 0:

        print(
            "Missing values found"
        )


        numeric_cols = df.select_dtypes(
            include=["number"]
        ).columns


        for col in numeric_cols:

            df[col] = df[col].fillna(
                df[col].median()
            )



        categorical_cols = df.select_dtypes(
            exclude=["number"]
        ).columns


        for col in categorical_cols:

            df[col] = df[col].fillna(
                df[col].mode()[0]
            )


        print(
            "Missing values filled"
        )


    else:

        print(
            "No missing values"
        )



    # ---------------------------------
    # 5. Find categorical columns
    # ---------------------------------

    categorical_columns = df.select_dtypes(
        include=["object"]
    ).columns


    print(
        "Categorical columns:",
        list(categorical_columns)
    )



    # ---------------------------------
    # 6. One Hot Encoding
    # ---------------------------------

    if len(categorical_columns) > 0:


        if training:


            print(
                "Creating encoder..."
            )


            encoder = OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            )


            encoded = encoder.fit_transform(
                df[categorical_columns]
            )


            encoded_df = pd.DataFrame(
                encoded,
                columns=encoder.get_feature_names_out(
                    categorical_columns
                )
            )


            df = df.drop(
                columns=categorical_columns
            )


            df = pd.concat(
                [
                    df.reset_index(drop=True),
                    encoded_df.reset_index(drop=True)
                ],
                axis=1
            )


            os.makedirs(
                MODEL_DIR,
                exist_ok=True
            )


            joblib.dump(
                encoder,
                ENCODER_PATH
            )


            print(
                "Encoder saved"
            )



        else:


            print(
                "Loading encoder"
            )


            encoder = joblib.load(
                ENCODER_PATH
            )


            encoded = encoder.transform(
                df[categorical_columns]
            )


            encoded_df = pd.DataFrame(
                encoded,
                columns=encoder.get_feature_names_out(
                    categorical_columns
                )
            )


            df = df.drop(
                columns=categorical_columns
            )


            df = pd.concat(
                [
                    df.reset_index(drop=True),
                    encoded_df.reset_index(drop=True)
                ],
                axis=1
            )


    else:

        print(
            "No categorical columns"
        )



    # ---------------------------------
    # 7. Add target back
    # ---------------------------------

    df.reset_index(
        drop=True,
        inplace=True
    )


    print(
        "Final Shape:",
        df.shape
    )


    print(
        "========== PREPROCESSING COMPLETED ==========\n"
    )


    return df