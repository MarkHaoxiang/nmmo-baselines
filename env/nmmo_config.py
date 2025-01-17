import nmmo

from lib.team.team_loader import TeamLoader

class NmmoMoveConfig(
    nmmo.config.Medium,
    nmmo.config.Terrain,
    nmmo.config.Resource,
    nmmo.config.Progression,
    nmmo.config.Equipment,
    nmmo.config.Item,
    nmmo.config.Exchange,
  ):
  def __init__(
      self,
      team_helper,
      num_maps=5,
      maps_path=None,
      max_episode_length=1024,
      death_fog_tick=None,
      **args
      ):

    super().__init__()

    self.PROVIDE_ACTION_TARGETS = True
    self.MAP_FORCE_GENERATION = False
    self.PLAYER_N = team_helper.num_teams * len(team_helper.teams[0])
    self.HORIZON = max_episode_length
    self.MAP_N = num_maps
    self.PLAYER_DEATH_FOG = death_fog_tick
    if maps_path is not None:
      self.PATH_MAPS = maps_path
    self.PLAYER_LOADER = lambda config: TeamLoader(config, team_helper)

class NmmoCombatConfig(NmmoMoveConfig, nmmo.config.Combat):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

# class NmmoNPCConfig(NmmoCombatConfig, nmmo.config.NPC):
#   def __init__(self, *args, **kwargs):
#     super().__init__(*args, **kwargs)
#     self.NPC_N = kwargs["num_npcs"]

# class NmmoProffessionConfig(NmmoNPCConfig, nmmo.config.Profession):
#   pass

def nmmo_config(team_helper, args):
  config_cls = NmmoMoveConfig
  if args["combat_enabled"]:
    config_cls = NmmoCombatConfig

  return config_cls(team_helper, **args)

