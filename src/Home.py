import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Local imports
from utils import get_data as d

# Title of the app
st.title("FPL Analysis")

# Initialise session state variables
st.session_state.team_id = ""
st.session_state.last_gameweek = 0

# Get data - user input
st.session_state.team_id = st.text_input(label="Enter your team ID")
st.markdown("Your team ID is the number found in the url on the Points page of the FPL website, e.g. fantasy.premierleague.com/entry/**2368852**/event/7")
st.session_state.last_gameweek = int(st.text_input(label="What was the most recent gameweek? e.g. 7", max_chars=2))

if st.session_state.team_id and st.session_state.last_gameweek:
    team_name, points, average_points, highest_points, gameweek_rank, overall_rank, team_value, transfers, transfers_cost, captain, captain_points, total_points_per_line_season = d.get_data(team_id = st.session_state.team_id, last_gameweek = st.session_state.last_gameweek)

    gameweek = np.arange(1, st.session_state.last_gameweek+1)

    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(11.69, 10)) #fig size A4 in inches figsize=(11.69,8.27)
    fig.suptitle("Team performance : " + team_name)
    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.3, hspace=0.4)

    ### Team points
    ax1.plot(gameweek, points, color='b', label='Team FPL points')
    ax1.plot(gameweek, average_points, color='black', label='Average FPL points')
    ax1.plot(gameweek, highest_points, color='r', label='Highest FPL points')
    ax1.set_xlabel('Gameweek')
    ax1.set_ylabel('FPL points')
    ax1.legend(loc='best', frameon=True, prop={'size':6})

    ### Team rank
    gameweekRank = np.array(gameweek_rank)
    ax2.bar(gameweek, gameweekRank, color='b', label='GW Rank', width=0.5)
    ax2.plot(gameweek, overall_rank, color='r', label='Overall rank')
    ax2.set_ylim(ymin=0)
    ax2.set_ylim(ymax=max(gameweekRank + 400000))
    ax2.get_yaxis().get_major_formatter().set_scientific(False)
    ax2.set_xlabel('Gameweek')
    ax2.set_ylabel('Rank')
    ax2.legend(loc='best', frameon=True, prop={'size':6})
    rects = ax2.patches
    for rect in rects:
        height = rect.get_height()
        ax2.text(rect.get_x() + rect.get_width() / 2, height + 100000, height, ha='center', va='bottom', size=6)

    ### Team value
    ax3.bar(gameweek, list(map(lambda x: x/10, team_value)), width=0.5, color='b')
    ax3.set_ylim(ymin=min(list(map(lambda x: x/10, team_value)))-0.5)
    ax3.set_ylim(ymax=max(list(map(lambda x: x/10, team_value)))+0.5)
    ax3.set_xlabel('Gameweek')
    ax3.set_ylabel('Team Value (incl. bank)')
    rects = ax3.patches
    labels = [sum(x) for x in zip(list(map(lambda x: round(x/10, 1), team_value)))]
    for rect, label in zip(rects, labels):
        height = rect.get_height()
        ax3.text(rect.get_x() + rect.get_width() / 2, height + 0.1, label, ha='center', va='bottom', size=6)

    ### Team transfers
    ax44 = ax4.twinx()
    ax4.bar(gameweek, transfers, color='b', label='Number of transfers', width=0.5)
    ax44.plot(gameweek, transfers_cost, color='r', label='Transfers cost')
    ax4.set_xlabel('Gameweek')
    ax4.set_ylabel('Number of transfers')
    ax44.set_ylabel('Transfers cost')
    ax4.legend(loc=2, frameon=True, prop={'size':6})
    ax44.legend(loc=1, frameon=True, prop={'size':6})
    ax44.set_ylim(ymin=0)
    ax44.set_ylim(ymax=max(transfers_cost)+1)
    ax4.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax44.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    ### Captain points
    captain_points = np.array(captain_points)
    captain_display = []
    for n in range(0, st.session_state.last_gameweek):
        captain_display.append(str(n+1) + " - " + captain[n])
    mask1 = captain_points > 3
    mask2 = captain_points <= 3
    ax5.bar(gameweek[mask1], list(map(lambda x: x*2, captain_points[mask1])), width=0.5, color='green')
    ax5.bar(gameweek[mask2], list(map(lambda x: x*2, captain_points[mask2])), width=0.5, color='firebrick')
    ax5.set_ylim(ymin=0)
    ax5.set_ylim(ymax=max(list(map(lambda x: x*2, captain_points)))+5)
    ax5.set_xticks(gameweek)
    ax5.set_xticklabels(captain_display, rotation=90, ha="right", size=6)
    ax5.set_ylabel('Captain FPL points')
    rects = ax5.patches
    for rect in rects:
        height = rect.get_height()
        ax5.text(rect.get_x() + rect.get_width() / 2, height + 0.6, height, ha='center', va='bottom', size=6)

    # ### Points per position
    # positions = list(total_points_per_line_season.keys())
    # points_pos = list(total_points_per_line_season.values())
    # colors = ['#f1d18a', '#73b1c1', '#588d9c', '#36626a']

    # def func(pct, allvals):
    #     absolute = int(pct/100.*np.sum(allvals))
    #     return "{:.1f}%\n({:d} pts)".format(pct, absolute)

    # wedges, texts, autotexts = ax6.pie(points_pos, autopct=lambda pct: func(pct, points_pos),
    #                                 textprops=dict(color="k"), colors=colors)

    # ax6.legend(wedges, positions,
    #         title="Positions",
    #         loc="center left",
    #         bbox_to_anchor=(0.92, 0, 0.5, 1))

    # ax6.set_xlabel("Points per position over the season")

    st.pyplot(fig)

else:
    st.info("Enter your team ID and the most recent GW to get started!")
