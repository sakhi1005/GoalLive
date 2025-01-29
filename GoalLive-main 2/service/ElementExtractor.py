import datetime

from bs4 import BeautifulSoup

from dtos.BroadcastOption import BroadcastOption
from dtos.Competition import Competition
from dtos.Match import Match
from dtos.Team import Team
from utils.ImageUtil import ImageUtil


def parse_html(html_content, date) -> [Competition]:
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize a list to hold competition data
    competitions = []

    # Find all competition blocks
    competition_blocks = soup.find_all('div', class_='competition_competition__wbjsu')

    for comp_block in competition_blocks:
        # Extract competition name
        comp_name_tag = comp_block.find('a', class_='competition_name__O93QA')
        if comp_name_tag:
            # Remove the logo div to get the pure competition name
            comp_logo_div = comp_name_tag.find('div', class_='competition_logo-wrapper__tejNa')
            if comp_logo_div:
                comp_logo_div.extract()  # Remove the logo div from the tag
            competition_name = comp_name_tag.get_text(strip=True)

            # Initialize a list to hold match data
            matches = []

            # Find all match rows within the competition block
            match_rows = comp_block.find_all('div', class_='row_row__pwLvU row')

            for match_row in match_rows:
                # Extract match time
                match_time_datetime = extract_time(match_row, date)

                # Extract home and away team names
                home_team_div = match_row.find('div', class_='team_team-a__KZ1AE')
                away_team_div = match_row.find('div', class_='team_team-b__6xMTs')

                # extract broadcast options
                broadcast_option = extract_broadcast_option(match_row)
                if home_team_div and away_team_div:
                    # need both the sides to create the fixture
                    home_team, away_team = extract_team(home_team_div), extract_team(away_team_div)
                    # Add the match to the matches list
                    matches.append(
                        Match(
                            home_team=home_team,
                            away_team=away_team,
                            match_time=match_time_datetime,
                            broadcast_option=broadcast_option,
                        )
                    )

            # Add the competition and its matches to the competitions list
            competitions.append(Competition(competition_name=competition_name, matches=matches))
    return competitions

''' -------------------------------------------- HELPER METHODS ---------------------------------------------------- '''

def extract_time(match_row, date) -> datetime.datetime | None:
    time_tag = match_row.find('time', class_='start-date_start-date__8rMB6')
    match_time = time_tag.get_text(strip=True) if time_tag else None
    if match_time is not None:
        # if this tag is not there, then the match has probably ended
        # print(f"=======DATE TYPE {type(date)} MATCH TIME TYPE {type(match_time)}=======")
        return datetime.datetime.strptime(date + " " + match_time, '%Y-%m-%d %H:%M')
    return None


def extract_broadcast_option(match_row):
    '''
    :param match_row:
    :return: broadcast options with name, logo and link
    '''
    broadcast_option_tag = match_row.find('a', class_='tv-channel_channel__obfuL tv-channel')
    if broadcast_option_tag:
        broadcast_option_name = broadcast_option_tag.find('span', class_='tv-channel_channel-name__tbVeb').get_text(strip=True)
        broadcast_url = broadcast_option_tag['href']
        broadcast_logo = broadcast_option_tag.find('img', class_='tv-channel_logo__DdEkB')['src']
        return BroadcastOption(broadcast_option_name, broadcast_url, broadcast_logo)
    return None

def extract_team(div):
    team_crest_url = None
    name = div.find('h4', class_='name_name__qsruk').get_text(strip=True)
    team_image_img = div.find('img', class_='crest team-crest_crest__Jp9_k')
    if team_image_img:
        team_image_url = team_image_img['src']
        team_crest_url = ImageUtil.get_cdn_url(team_image_url)
    return Team(name, team_crest_url)






