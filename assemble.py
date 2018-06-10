import os
import settings
import pandas as pd

HEADERS = {
    "Acquisition": [
        "id",
        "channel",
        "seller",
        "interest_rate",
        "balance",
        "loan_term",
        "origination_date",
        "first_payment_date",
        "ltv",
        "cltv",
        "borrower_count",
        "dti",
        "borrower_credit_score",
        "first_time_homebuyer",
        "loan_purpose",
        "property_type",
        "unit_count",
        "occupancy_status",
        "property_state",
        "zip",
        "insurance_percentage",
        "product_type",
        "co_borrower_credit_score",
        "mortgage_insurance_type",
        "relocation_mortgage_indicator"
    ],
    "Performance": [
        "id",
        "reporting_period",
        "servicer_name",
        "interest_rate",
        "balance",
        "loan_age",
        "months_to_maturity",
        "maturity_date",
        "msa",
        "delinquency_status",
        "modification_flag",
        "zero_balance_code",
        "zero_balance_date",
        "last_paid_installment_date",
        "foreclosure_date",
        "disposition_date",
        "foreclosure_costs",
        "property_repair_costs",
        "recovery_costs",
        "misc_costs",
        "tax_costs",
        "sale_proceeds",
        "credit_enhancement_proceeds",
        "repurchase_proceeds",
        "other_foreclosure_proceeds",
        "non_interest_bearing_balance",
        "principal_forgiveness_balance",
        "repurchase_make_whole_proceeds_flag",
        "foreclosure_principal_write-off_amount",
        "servicing_activity_indicator"
    ]
}

SELECT = {
    "Acquisition": HEADERS["Acquisition"],
    "Performance": [
        "id",
        "foreclosure_date"
    ]
}

def concatenate(prefix="Acquisition"):
    files = os.listdir(settings.DATA_DIR)
    full = []

    for f in files:
        if not f.startswith(prefix):
            continue
        df = pd.read_csv(os.path.join(settings.DATA_DIR, f),
                         sep='|',
                         header=None,
                         names=HEADERS[prefix],
                         index_col=False)
        df = df[SELECT[prefix]]
        full.append(df)

    full = pd.concat(full, axis=0)
    print("ok")

    full.to_csv(os.path.join(settings.PROCESSED_DIR, "{}.txt".format(prefix)),
                header=SELECT[prefix],
                sep='|',
                index=False)

if __name__ == "__main__":
    concatenate("Acquisition")
    concatenate("Performance")