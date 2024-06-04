import os.path

import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle
from PIL import Image, ImageDraw

from src.server.helpers import png_to_bmp
from datetime import datetime

IMG_DIR = os.path.join(os.getcwd(), "img")
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)
LOWEST_PRICE_PATH = os.path.join(IMG_DIR, "lowest_price.png")
BAR_PLOT_PATH = os.path.join(IMG_DIR, "bar_plot.png")
CIRCULAR_GAUGE_PATH = os.path.join(IMG_DIR, "circular_gauge.png")

# Constants
# Image size
IMAGE_SIZE = (1200, 700)

# Subplot positions
BARPLOT_POS = (240, 20)
LOWEST_PRICE_POS = (50, 250)
CIRCULAR_GAUGE_POS = (50, 50)

# Figure sizes
BAR_FIGSIZE = (11, 6)
CIRCLE_FIGSIZE = (2.5, 2.5)

# Elements

TIME_FONTSIZE = 18

BARGRAPH_COLOR = "#444444"

CIRCLE_RADIUS = 0.4
CIRCLE_COLOR = '#aaaaaa'


class SimpleDashboardBuilder:

    def build_dashboard(self, df: pd.DataFrame) -> str:

        # Function to create the circular gauge element
        def create_circular_gauge(value, current_hour, max_value=1):
            fig, ax = plt.subplots(
                figsize=CIRCLE_FIGSIZE, subplot_kw={"aspect": "equal"}
            )
            ax.axis("off")

            # Draw the full circle in light gray
            ax.add_patch(Circle((0.5, 0.5), CIRCLE_RADIUS, color=CIRCLE_COLOR))

            # Draw the arc in black
            angle = 360 * (value % 1 / max_value)

            print(f"{value=}\n{angle=}")
            arc = Arc(
                (0.5, 0.5),
                0.8,
                0.8,
                angle=0,
                theta1=0,
                theta2=angle,
                color="black",
                linewidth=8,
            )
            ax.add_patch(arc)

            # Add the text in black
            ax.text(
                0.5,
                0.4,
                f"{value:.0f}ct",
                horizontalalignment="center",
                verticalalignment="center",
                fontsize=25,
                color="black",
            )
            ax.text(
                0.5,
                0.65,
                f"{current_hour}h",
                horizontalalignment="center",
                verticalalignment="center",
                fontsize=TIME_FONTSIZE,
                color="black",
            )

            # Save the circular gauge as an image
            fig.savefig(
                CIRCULAR_GAUGE_PATH,
                bbox_inches="tight",
                pad_inches=0,
                transparent=True,
            )
            plt.close(fig)

        def create_lowest_price_indicator(df):
            lowest_price = df["Preis in ct"].min()
            lowest_price_hour = df.loc[df["Preis in ct"].idxmin(), "hour"]
            fig, ax = plt.subplots(
                figsize=CIRCLE_FIGSIZE, subplot_kw={"aspect": "equal"}
            )
            ax.axis("off")

            # Draw the full circle in light gray
            ax.add_patch(Circle((0.5, 0.5), CIRCLE_RADIUS, color=CIRCLE_COLOR))

            # Add the text in black
            ax.text(
                0.5,
                0.4,
                f"{lowest_price:.0f}ct",
                horizontalalignment="center",
                verticalalignment="center",
                fontsize=25,
                color="black",
            )
            ax.text(
                0.5,
                0.65,
                f"\$ {lowest_price_hour}h \$",
                horizontalalignment="center",
                verticalalignment="center",
                fontsize=TIME_FONTSIZE,
                color="black",
            )

            # Save the circular gauge as an image
            fig.savefig(
                LOWEST_PRICE_PATH,
                bbox_inches="tight",
                pad_inches=0,
                transparent=True,
            )
            plt.close(fig)

        # Function to create the bar plot from a DataFrame
        def create_bar_plot(df):
            current_hour = datetime.now().hour
            current_day = datetime.now().day

            hours = df["hour"]
            days = df["day"]
            time = df["Zeit"]
            prices = df["Preis in ct"]

            fig, ax = plt.subplots(figsize=BAR_FIGSIZE)

            # Draw bars in grayscale
            ax.fill_between(
                time, prices, step="mid", alpha=0.5, color=BARGRAPH_COLOR, label="Heute"
            )
            if current_hour in hours.values and current_day in days.values:
                current_price = df[df["hour"] == current_hour][
                    df["day"] == current_day
                ]["Preis in ct"].iloc[0]
                ax.bar(
                    current_hour,
                    current_price,
                    color="black",
                    edgecolor="white",
                    linewidth=2,
                )
            lowest_price_time = df[df["Preis in ct"] == df["Preis in ct"].min()]["Zeit"]
            lowest_price = df[df["Preis in ct"] == df["Preis in ct"].min()][
                "Preis in ct"
            ]
            ax.bar(
                lowest_price_time,
                lowest_price,
                color="white",
                edgecolor="black",
                linewidth=2,
            )

            ax.set_xticklabels(
                [str(x) if i % 4 == 0 else "" for i, x in enumerate(list(df["hour"]))],
                rotation=45,
                horizontalalignment="right",
            )

            ax.tick_params(axis="y", labelsize=15)
            ax.tick_params(axis="x", labelsize=15)
            ax.set_ylabel("cent")
            ax.set_title(f"{datetime.now().strftime('%d.%m.%Y')}", fontsize=20)

            ax.set_ylim(15, 45)

            # Save the plot as an image
            fig.savefig(BAR_PLOT_PATH, bbox_inches="tight", format="png")
            plt.close(fig)

        # Function to create the dashboard
        def create_dashboard(df):
            # Get the last value for the circular gauge
            current_hour = datetime.now().hour
            current_day = datetime.now().day

            # Find the value for the current hour
            latest_value = df[df["hour"] == current_hour][df["day"] == current_day][
                "Preis in ct"
            ].iloc[0]
            # Create the images
            create_circular_gauge(latest_value, current_hour)
            create_lowest_price_indicator(df)
            create_bar_plot(df)

            # Combine the images using Pillow
            dashboard_image = Image.new(
                "L", IMAGE_SIZE, color="white"
            )  # 'L' mode for grayscale
            draw = ImageDraw.Draw(dashboard_image)

            # Load the created images
            circular_gauge = Image.open(CIRCULAR_GAUGE_PATH)
            bar_plot = Image.open(BAR_PLOT_PATH)
            lowest_price = Image.open(LOWEST_PRICE_PATH)
            # Paste the images onto the dashboard
            dashboard_image.paste(
                circular_gauge, CIRCULAR_GAUGE_POS, circular_gauge
            )  # The circular gauge
            dashboard_image.paste(lowest_price, LOWEST_PRICE_POS)  # The lowest price
            dashboard_image.paste(bar_plot, BARPLOT_POS)  # The bar plot

            # Save the final dashboard image
            dashboard_path = self.get_image_path()
            dashboard_image.save(dashboard_path)
            # convert the png file to bmp
            bmp_path = png_to_bmp(
                dashboard_path, dashboard_path.replace(".png", ".bmp")
            )
            return bmp_path

        return create_dashboard(df)

    def build_legacy_dashboard(self, tibber_df: pd.DataFrame) -> str:
        print("Building simple dashboard")
        print(f"{tibber_df=}"[0:100])

        # Create a broad barplot
        # sns.set_theme(rc={'figure.figsize': (11.7, 8.27)})
        # sns.set_context("paper", font_scale=0.5)
        # We want to 'Zeit' as the x axis, but 'hour' as the label in jumps of 4 hours

        tibber_plot = sns.barplot(data=tibber_df, x="Zeit", y="Preis in ct")
        tibber_plot.set(xlabel="Zeit (Stunde)", ylabel="Price in ct")
        tibber_plot.set_xticklabels(
            [
                str(x) if i % 4 == 0 else ""
                for i, x in enumerate(list(tibber_df["hour"]))
            ],
            rotation=45,
            horizontalalignment="right",
        )
        tibber_plot.set_title(
            f'Kostenprognose am {datetime.now().strftime("%Y-%m-%d")}'
        )
        tibber_plot.set_ylim(15, 45)

        tibber_plot.axhline(
            tibber_df["tax"].mean() * 100, ls="--", color="r", label="Kostenlos"
        )

        img_path = self.get_image_path()
        tibber_plot.get_figure().savefig(img_path, format="png")
        # convert the png file to bmp
        bmp_path = png_to_bmp(img_path, img_path.replace(".png", ".bmp"))
        return bmp_path

    @staticmethod
    def get_image_path():
        # Save the plot as an image

        img_name = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_tibber_plot.png"
        img_path = os.path.join(IMG_DIR, img_name)
        return img_path
