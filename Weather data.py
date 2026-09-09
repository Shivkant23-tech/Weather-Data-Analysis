# ============================================================
# Weather Data Analysis Project
# ============================================================
# Purpose:
#   Analyze weather data using Python, Pandas, NumPy,
#   Matplotlib and Seaborn.
#
# Pipeline:
#   1. Load data
#   2. Validate data
#   3. Clean data
#   4. Analyze data
#   5. Visualize data
#   6. Generate insights
#   7. Save professional report
# ============================================================

import os
import sys
from typing import Any

import pandas as pd
import matplotlib.pyplot as _plt
import seaborn as _sns


plt: Any = _plt
sns: Any = _sns


Analysis = dict[str, Any]


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

DATA_FILE = "Weather_data.csv"
OUTPUT_DIR = "output"

TEMPERATURE_CHART = os.path.join(
    OUTPUT_DIR, "temperature_trend.png"
)

CONDITION_CHART = os.path.join(
    OUTPUT_DIR, "weather_conditions.png"
)

REPORT_FILE = os.path.join(
    OUTPUT_DIR, "analysis_report.txt"
)


# ------------------------------------------------------------
# Create output directory
# ------------------------------------------------------------

def create_output_directory():
    """Create output folder if it does not exist."""

    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        print("✓ Output directory ready.")

    except OSError as error:
        print(f"Error creating output directory: {error}")
        sys.exit(1)


# ------------------------------------------------------------
# Load Dataset
# ------------------------------------------------------------

def load_data(file_path: str) -> pd.DataFrame:
    """Load weather dataset from CSV file."""

    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Dataset not found: {file_path}"
            )

        df = pd.read_csv(file_path)

        if df.empty:
            raise ValueError("The dataset is empty.")

        print(f"✓ Dataset loaded successfully.")
        print(f"  Rows: {df.shape[0]}")
        print(f"  Columns: {df.shape[1]}")

        return df

    except FileNotFoundError as error:
        print(f"Error: {error}")
        sys.exit(1)

    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
        sys.exit(1)

    except pd.errors.ParserError:
        print("Error: Unable to parse the CSV file.")
        sys.exit(1)

    except Exception as error:
        print(f"Unexpected error while loading data: {error}")
        sys.exit(1)


# ------------------------------------------------------------
# Validate Dataset
# ------------------------------------------------------------

def validate_data(df: pd.DataFrame) -> bool:
    """Validate required columns and data structure."""

    required_columns = [
        "Date",
        "Temperature",
        "Humidity",
        "WindSpeed",
        "Pressure",
        "WeatherCondition"
    ]

    print("\n--- Data Validation ---")

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print(
            "Error: Missing required columns:",
            missing_columns
        )
        sys.exit(1)

    print("✓ All required columns are present.")

    print(f"✓ Duplicate rows: {df.duplicated().sum()}")

    print("\nMissing values:")
    print(df.isnull().sum())

    return True


# ------------------------------------------------------------
# Clean Dataset
# ------------------------------------------------------------

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare weather dataset."""

    print("\n--- Data Cleaning ---")

    df = df.copy()

    # Remove duplicate records
    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:
        df = df.drop_duplicates()
        print(f"✓ Removed {duplicate_count} duplicate rows.")

    # Convert Date column
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    # Convert numerical columns
    numeric_columns = [
        "Temperature",
        "Humidity",
        "WindSpeed",
        "Pressure"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Remove rows where critical values are missing
    before = len(df)

    df = df.dropna(
        subset=[
            "Date",
            "Temperature",
            "Humidity",
            "WindSpeed",
            "Pressure",
            "WeatherCondition"
        ]
    )

    removed_rows = before - len(df)

    if removed_rows > 0:
        print(f"✓ Removed {removed_rows} invalid rows.")

    # Validate realistic weather ranges
    df = df[
        (df["Humidity"] >= 0) &
        (df["Humidity"] <= 100)
    ]

    df = df[
        df["Pressure"] > 0
    ]

    # Sort by date
    df = df.sort_values("Date")

    df = df.reset_index(drop=True)

    print(f"✓ Clean dataset contains {len(df)} rows.")

    return df


# ------------------------------------------------------------
# Analyze Dataset
# ------------------------------------------------------------

def analyze_data(df: pd.DataFrame) -> Analysis:
    """Perform statistical weather analysis."""

    print("\n--- Weather Analysis ---")

    analysis: Analysis = {}

    # Temperature statistics
    analysis["average_temperature"] = df[
        "Temperature"
    ].mean()

    analysis["maximum_temperature"] = df[
        "Temperature"
    ].max()

    analysis["minimum_temperature"] = df[
        "Temperature"
    ].min()

    # Humidity
    analysis["average_humidity"] = df[
        "Humidity"
    ].mean()

    # Wind
    analysis["average_wind_speed"] = df[
        "WindSpeed"
    ].mean()

    analysis["maximum_wind_speed"] = df[
        "WindSpeed"
    ].max()

    # Pressure
    analysis["average_pressure"] = df[
        "Pressure"
    ].mean()

    # Weather condition frequency
    condition_counts: pd.Series = df[
        "WeatherCondition"
    ].value_counts()

    analysis["most_common_condition"] = (
        condition_counts.index[0]
    )

    analysis["condition_counts"] = condition_counts

    # Temperature range
    analysis["temperature_range"] = (
        analysis["maximum_temperature"]
        - analysis["minimum_temperature"]
    )

    # Correlation
    analysis["temperature_humidity_correlation"] = (
        df["Temperature"].corr(df["Humidity"])
    )

    return analysis


# ------------------------------------------------------------
# Display Analysis
# ------------------------------------------------------------

def display_analysis(analysis: Analysis) -> None:

    print("\n========================================")
    print("        WEATHER ANALYSIS RESULTS")
    print("========================================")

    print(
        f"Average Temperature: "
        f"{analysis['average_temperature']:.2f} °C"
    )

    print(
        f"Maximum Temperature: "
        f"{analysis['maximum_temperature']:.2f} °C"
    )

    print(
        f"Minimum Temperature: "
        f"{analysis['minimum_temperature']:.2f} °C"
    )

    print(
        f"Temperature Range: "
        f"{analysis['temperature_range']:.2f} °C"
    )

    print(
        f"Average Humidity: "
        f"{analysis['average_humidity']:.2f}%"
    )

    print(
        f"Average Wind Speed: "
        f"{analysis['average_wind_speed']:.2f}"
    )

    print(
        f"Maximum Wind Speed: "
        f"{analysis['maximum_wind_speed']:.2f}"
    )

    print(
        f"Average Pressure: "
        f"{analysis['average_pressure']:.2f}"
    )

    print(
        f"Most Common Weather Condition: "
        f"{analysis['most_common_condition']}"
    )

    print(
        f"Temperature-Humidity Correlation: "
        f"{analysis['temperature_humidity_correlation']:.2f}"
    )


# ------------------------------------------------------------
# Visualization 1: Temperature Trend
# ------------------------------------------------------------

def create_temperature_chart(df: pd.DataFrame) -> None:

    try:

        plt.figure(figsize=(12, 6))

        plt.plot(
            df["Date"],
            df["Temperature"],
            marker="o",
            linewidth=2
        )

        plt.title(
            "Daily Temperature Trend",
            fontsize=16,
            fontweight="bold"
        )

        plt.xlabel("Date")
        plt.ylabel("Temperature (°C)")

        plt.xticks(rotation=45)

        plt.grid(
            True,
            alpha=0.3
        )

        plt.tight_layout()

        plt.savefig(
            TEMPERATURE_CHART,
            dpi=300
        )

        plt.close()

        print(
            f"✓ Temperature chart saved: "
            f"{TEMPERATURE_CHART}"
        )

    except Exception as error:
        print(
            f"Error creating temperature chart: {error}"
        )


# ------------------------------------------------------------
# Visualization 2: Weather Condition Distribution
# ------------------------------------------------------------

def create_condition_chart(df: pd.DataFrame) -> None:

    try:

        plt.figure(figsize=(10, 6))

        sns.countplot(
            data=df,
            x="WeatherCondition",
            order=df["WeatherCondition"].value_counts().index
        )

        plt.title(
            "Weather Condition Distribution",
            fontsize=16,
            fontweight="bold"
        )

        plt.xlabel("Weather Condition")
        plt.ylabel("Number of Days")

        plt.tight_layout()

        plt.savefig(
            CONDITION_CHART,
            dpi=300
        )

        plt.close()

        print(
            f"✓ Weather condition chart saved: "
            f"{CONDITION_CHART}"
        )

    except Exception as error:
        print(
            f"Error creating condition chart: {error}"
        )


# ------------------------------------------------------------
# Generate Insights
# ------------------------------------------------------------

def generate_insights(analysis: Analysis) -> list[str]:

    print("\n--- Key Insights ---")

    insights: list[str] = []

    average_temp = analysis["average_temperature"]
    max_temp = analysis["maximum_temperature"]
    min_temp = analysis["minimum_temperature"]
    average_humidity = analysis["average_humidity"]
    most_common = analysis["most_common_condition"]

    insights.append(
        f"The average temperature during the analyzed "
        f"period was {average_temp:.2f} °C."
    )

    insights.append(
        f"The highest recorded temperature was "
        f"{max_temp:.2f} °C."
    )

    insights.append(
        f"The lowest recorded temperature was "
        f"{min_temp:.2f} °C."
    )

    insights.append(
        f"The temperature varied by "
        f"{analysis['temperature_range']:.2f} °C "
        f"between the minimum and maximum values."
    )

    insights.append(
        f"The average humidity was "
        f"{average_humidity:.2f}%."
    )

    insights.append(
        f"'{most_common}' was the most frequently "
        f"observed weather condition."
    )

    correlation = (
        analysis["temperature_humidity_correlation"]
    )

    if correlation < -0.5:

        insights.append(
            "Temperature and humidity show a strong "
            "negative relationship in this dataset."
        )

    elif correlation > 0.5:

        insights.append(
            "Temperature and humidity show a strong "
            "positive relationship in this dataset."
        )

    else:

        insights.append(
            "Temperature and humidity show a weak or "
            "moderate relationship in this dataset."
        )

    for number, insight in enumerate(insights, 1):

        print(f"{number}. {insight}")

    return insights


# ------------------------------------------------------------
# Generate Professional Report
# ------------------------------------------------------------

def generate_report(
    df: pd.DataFrame,
    analysis: Analysis,
    insights: list[str]
) -> None:

    try:

        with open(
            REPORT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            file.write("=" * 60 + "\n")
            file.write("             WEATHER DATA ANALYSIS REPORT\n")
            file.write("=" * 60 + "\n\n")

            file.write("1. DATASET OVERVIEW\n")
            file.write("-" * 40 + "\n")

            file.write(
                f"Number of records: {len(df)}\n"
            )

            file.write(
                f"Number of columns: {len(df.columns)}\n"
            )

            file.write(
                f"Analysis period: "
                f"{df['Date'].min().date()} to "
                f"{df['Date'].max().date()}\n\n"
            )

            file.write("2. KEY METRICS\n")
            file.write("-" * 40 + "\n")

            file.write(
                f"Average Temperature: "
                f"{analysis['average_temperature']:.2f} °C\n"
            )

            file.write(
                f"Maximum Temperature: "
                f"{analysis['maximum_temperature']:.2f} °C\n"
            )

            file.write(
                f"Minimum Temperature: "
                f"{analysis['minimum_temperature']:.2f} °C\n"
            )

            file.write(
                f"Average Humidity: "
                f"{analysis['average_humidity']:.2f}%\n"
            )

            file.write(
                f"Average Wind Speed: "
                f"{analysis['average_wind_speed']:.2f}\n"
            )

            file.write(
                f"Maximum Wind Speed: "
                f"{analysis['maximum_wind_speed']:.2f}\n"
            )

            file.write(
                f"Average Pressure: "
                f"{analysis['average_pressure']:.2f}\n"
            )

            file.write(
                f"Most Common Condition: "
                f"{analysis['most_common_condition']}\n"
            )

            file.write(
                f"Temperature-Humidity Correlation: "
                f"{analysis['temperature_humidity_correlation']:.2f}\n\n"
            )

            file.write("3. WEATHER CONDITION COUNTS\n")
            file.write("-" * 40 + "\n")

            condition_counts: dict[str, int] = analysis.get(
                "condition_counts",
                {}
            )

            for condition, count in condition_counts.items():

                file.write(
                    f"{condition}: {count} days\n"
                )

            file.write("\n4. KEY INSIGHTS\n")
            file.write("-" * 40 + "\n")

            for number, insight in enumerate(
                insights,
                1
            ):

                file.write(
                    f"{number}. {insight}\n"
                )

            file.write("\n5. OUTPUT FILES\n")
            file.write("-" * 40 + "\n")

            file.write(
                "temperature_trend.png\n"
            )

            file.write(
                "weather_conditions.png\n"
            )

            file.write("\n")
            file.write("=" * 60 + "\n")
            file.write("End of Report\n")
            file.write("=" * 60 + "\n")

        print(
            f"✓ Professional report saved: {REPORT_FILE}"
        )

    except IOError as error:

        print(
            f"Error writing report: {error}"
        )


# ------------------------------------------------------------
# Main Pipeline
# ------------------------------------------------------------

def main():

    print("\n")
    print("=" * 60)
    print("             WEATHER DATA ANALYSIS")
    print("=" * 60)

    # Step 1: Create output folder
    create_output_directory()

    # Step 2: Load data
    df = load_data(DATA_FILE)

    # Step 3: Validate data
    validate_data(df)

    # Step 4: Clean data
    df = clean_data(df)

    # Stop if no usable data remains
    if df.empty:

        print(
            "Error: No valid data remains after cleaning."
        )

        sys.exit(1)

    # Step 5: Analyze data
    analysis = analyze_data(df)

    # Step 6: Display results
    display_analysis(analysis)

    # Step 7: Create visualizations
    print("\n--- Creating Visualizations ---")

    create_temperature_chart(df)

    create_condition_chart(df)

    # Step 8: Generate insights
    insights = generate_insights(analysis)

    # Step 9: Generate report
    print("\n--- Generating Report ---")

    generate_report(
        df,
        analysis,
        insights
    )

    print("\n")
    print("=" * 60)
    print("             ANALYSIS COMPLETED")
    print("=" * 60)

    print("\nGenerated files:")

    print(
        f"✓ {TEMPERATURE_CHART}"
    )

    print(
        f"✓ {CONDITION_CHART}"
    )

    print(
        f"✓ {REPORT_FILE}"
    )


# ------------------------------------------------------------
# Program Entry Point
# ------------------------------------------------------------

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:

        print("\nProgram stopped by user.")

    except Exception as error:

        print(
            f"\nUnexpected application error: {error}"
        )

        sys.exit(1)