import os
from typing import Callable, Dict, Tuple

from sports_api.config import Config


def league_id_to_name(league_id: int) -> str:
    """
    Map league IDs to their names for file naming purposes.
    """
    league_mapping = {
        4328: "premier_league",
        4331: "bundesliga",
        4332: "serie_a",
        4334: "ligue_1",
        4335: "laliga",
        # Add more leagues as needed
    }
    return league_mapping.get(league_id, f"league_{league_id}")


def _get_common_components(config: Config, league_id: int = None, season: str = None) -> Tuple[str, str, str]:
    """
    Extract common components used by all path generators.
    """
    base_path = config.get_output_settings()['output_path']
    league_name = league_id_to_name(league_id) if league_id else ""
    formatted_season = season.replace("-", "_") if season else ""
    return base_path, league_name, formatted_season


def _generate_rounds_path(config: Config, league_id: int = None, season: str = None,
                          round_num: int = None, **kwargs) -> Tuple[str, str]:
    """
    Generate path for rounds data.
    """
    base_path, league_name, formatted_season = _get_common_components(config, league_id, season)

    directory = os.path.join(base_path, "rounds", league_name, formatted_season)

    if round_num is None:
        start_round = kwargs.get('start_round', 1)
        end_round = kwargs.get('end_round', 38)
        filename = f"{league_name}_{formatted_season}_rounds_{start_round}_to_{end_round}.json"
    else:
        filename = f"{league_name}_{formatted_season}_round_{round_num}.json"

    return directory, filename


def _generate_league_table_path(config: Config, league_id: int = None, season: str = None, **kwargs) -> Tuple[str, str]:
    """
    Generate path for league table data.
    """
    base_path, league_name, formatted_season = _get_common_components(config, league_id, season)

    directory = os.path.join(base_path, "tables", league_name, formatted_season)
    filename = f"{league_name}_{formatted_season}_table.json"

    return directory, filename


def _generate_season_matches_path(config: Config, league_id: int = None, season: str = None, **kwargs) -> Tuple[
    str, str]:
    """
    Generate path for season matches data.
    """
    base_path, league_name, formatted_season = _get_common_components(config, league_id, season)

    directory = os.path.join(base_path, "matches", league_name, formatted_season)
    filename = f"{league_name}_{formatted_season}_all_matches.json"

    return directory, filename


def _generate_default_path(config: Config, league_id: int = None, season: str = None, round_num: int = None,
                           **kwargs) -> Tuple[str, str]:
    """
    Generate default path for other data types.
    """
    base_path, league_name, formatted_season = _get_common_components(config, league_id, season)

    # Extract data_type from kwargs for default path generation
    data_type = kwargs.get('data_type', 'unknown')

    directory = os.path.join(base_path, data_type)
    filename = f"{data_type}_{league_name}_{formatted_season}.json"

    return directory, filename


# Registry of path generators
PATH_GENERATORS: Dict[str, Callable] = {
    "rounds": _generate_rounds_path,
    "league_table": _generate_league_table_path,
    "season_matches": _generate_season_matches_path,
    # Add more as needed
}


def generate_file_path(config: Config, data_type: str, league_id: int = None, season: str = None, round_num: int = None,
                       **kwargs) -> tuple[str, str]:
    """
    Generate appropriate file path and name based on the data type and parameters.
    """
    if not config:
        raise ValueError("Config object is required to generate file path.")

    generator_func = PATH_GENERATORS.get(data_type, _generate_default_path)

    # Pass data_type in kwargs for default generator
    if data_type not in PATH_GENERATORS:
        kwargs['data_type'] = data_type

    return generator_func(config, league_id=league_id, season=season, round_num=round_num, **kwargs)
