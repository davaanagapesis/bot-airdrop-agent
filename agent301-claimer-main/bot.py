import sys
import streamlit as st
import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import association_rules, apriori
import time

sys.dont_write_bytecode = True

from smart_airdrop_claimer import base
from core.info import get_info
from core.task import process_do_task, process_do_wheel_task
from core.spin import process_spin_wheel


# Agent class from the first code
class Agent:
    def __init__(self):
        # Get file directory
        self.data_file = base.file_path(file_name="data.txt")
        self.config_file = base.file_path(file_name="config.json")

        # Initialize line
        self.line = base.create_line(length=50)

        # Initialize banner
        self.banner = base.create_banner(game_name="Agent 301")

        # Get config
        self.auto_do_task = base.get_config(
            config_file=self.config_file, config_name="auto-do-task"
        )

        self.auto_do_wheel_task = base.get_config(
            config_file=self.config_file, config_name="auto-do-wheel-task"
        )

        self.auto_spin_wheel = base.get_config(
            config_file=self.config_file, config_name="auto-spin-wheel"
        )

    def run_agent_tasks(self):
        base.clear_terminal()
        print(self.banner)
        data = open(self.data_file, "r").read().splitlines()
        num_acc = len(data)
        base.log(self.line)
        base.log(f"{base.green}Number of accounts: {base.white}{num_acc}")

        for no, data in enumerate(data):
            base.log(self.line)
            base.log(f"{base.green}Account number: {base.white}{no+1}/{num_acc}")

            try:
                get_info(data=data)

                # Do task
                if self.auto_do_task:
                    base.log(f"{base.yellow}Auto Do Task: {base.green}ON")
                    process_do_task(data=data)
                else:
                    base.log(f"{base.yellow}Auto Do Task: {base.red}OFF")

                # Wheel task
                if self.auto_do_wheel_task:
                    base.log(f"{base.yellow}Auto Do Wheel Task: {base.green}ON")
                    process_do_wheel_task(data=data)
                else:
                    base.log(f"{base.yellow}Auto Do Wheel Task: {base.red}OFF")

                # Spin wheel
                if self.auto_spin_wheel:
                    base.log(f"{base.yellow}Auto Spin Wheel: {base.green}ON")
                    process_spin_wheel(data=data)
                else:
                    base.log(f"{base.yellow}Auto Spin Wheel: {base.red}OFF")

            except Exception as e:
                base.log(f"{base.red}Error: {base.white}{e}")

        print()
        wait_time = 60 * 60
        base.log(f"{base.yellow}Wait for {int(wait_time/60)} minutes!")
        time.sleep(wait_time)


# Streamlit and pandas functionalities from the second code
df = pd.read_csv("Groceries data.csv")
df['Date'] = pd.to_datetime(df['Date'])

df["month"] = df['Date'].dt.month
df["day"] = df['Date'].dt.weekday

df["month"].replace([i for i in range(1, 12 + 1)], ["January", "February", "March", "April",
                    "May", "June", "July", "August", "September", "October", "November", "December"], inplace=True)
df["day"].replace([i for i in range(6 + 1)], ["Monday", "Tuesday",
                  "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], inplace=True)


def get_data(month='', day=''):
    data = df.copy()
    filtered = data.loc[
        (data["month"].str.contains(month.title())) &
        (data["day"].str.contains(day.title()))
    ]
    return filtered if filtered.shape[0] else "No result!"


def user_input_features():
    item = st.sidebar.selectbox("Item", ['tropical fruit', 'whole milk', 'pip fruit', 'other vegetables',
                                         'rolls/buns', 'citrus fruit', 'beef', 'frankfurter',
                                         'chicken', 'butter', 'fruit/vegetable juice',
                                         'packaged fruit/vegetables', 'chocolate', 'specialty bar',
                                         'butter milk', 'bottled water', 'yogurt', 'sausage', 'brown bread',
                                         'hamburger meat', 'root vegetables', 'pork', 'pastry',
                                         'canned beer', 'berries', 'coffee', 'misc. beverages', 'ham',
                                         'turkey', 'curd cheese', 'red/blush wine',
                                         'frozen potato products', 'flour', 'sugar', 'frozen meals',
                                         'herbs', 'soda', 'detergent', 'grapes', 'processed cheese', 'fish',
                                         'sparkling wine', 'newspapers', 'curd', 'pasta', 'popcorn',
                                         'finished products', 'beverages', 'bottled beer', 'dessert',
                                         'dog food', 'specialty chocolate', 'condensed milk', 'cleaner',
                                         'white wine'])
    month = st.sidebar.select_slider("Month", [
                                     "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    day = st.sidebar.select_slider(
        'Day', ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], value="Sat")

    return month, day, item


def main():
    st.title("Agent 301 and Market Analysis")
    st.subheader("Streamlit Display")
    
    # Display the table
    month, day, item = user_input_features()
    data = get_data(month, day)
    
    try:
        st.text("")
        st.text("")
        st.dataframe(data)
    except:
        st.markdown("No result found!")
    
    # Run Agent tasks
    agent = Agent()
    agent.run_agent_tasks()


if __name__ == "__main__":
    main()
