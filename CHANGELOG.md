All notable changes to this project will be documented in this file.
# Changelog

## [0.2.6.7] - 2025-04-04
### Changed
- align object to 3d cursors now can added orientation
- align light to 3d cursors also has rotation
- light power uses same precision as light data property panel
- light size x an y use meters
- changed precision of props to match blender GUI props

## [0.2.6.6] - 2025-03-12
### Fixed
- operator to quick open prefences and other addons by adding name

### Added
- Quick find operator > open search and addon name it opens preference search with addon filled in
- Restart operator > useful for devolopers

## [0.2.6.5] - 2024-11-12
### Added
- operator to quickly orientate selection to 3dview cursor. Set scale and distance 

### Changed
- Temp removed maxid checker for store screen workspace (get_names_workspaces) names, issue arose

## [0.2.6.5] - 2024-11-11
### Fixed
- Issue with storeview viewloc going from Compositor to 3Dview

## v0.2.6
## 2024-04-04
### Fixed
- Store View issue, wasnt working some since new blender update (+/- 3.6)

## v0.2.5
## 2023-02-27
### Added
- operator to quickly orientate lights to 3dview cursor 

## v0.2.4
## 2023-05-09
### Added
- shortcut for 3 button enum, handy for laptop users

## [0.2.3] - 2022-09-23
### Added
- Opening prefs operator shows addon expanded

## [0.2.2] - 2022-01-21
### Changed
- WIP try to storre workspaces using ID, workspace is saved by alphabetical list. Causes issue on name change
  ^ Try to save names workspaces, issue is still present when name is changed. Workspaces dont have any info order  


## [0.2.1] - 2022-01-20
### Fixed
- Store view after looking at MACHIN3 method. I was close > Set store view as a default
- If workspace are not in default names, revert to a default name and interaction mode > needs work for keymaps

## [0.2.0] - 2021-08-05
### Fixed
- Menu operator for console > hode for OSX

## [0.1.9] - 2021-03-05
### Added
- Operator to go to file location > missing since old blender

## [0.1.9] - 2021-02-26
### Added
- Show console (Windows)
- Viewport Render Frames

## [0.1.8] - 2020-03-20
### Fixed
- Warning error Panel class


## [0.1.7] - 2020-03-17
### Fixed
- Space in enumproperty

## [0.1.6] - 2020-03-11
### Fixed
- Render Display changed named

### Changed
- Moved Render in to render section

## [0.1.5] - 2020-01-15
### Fixed
- Viewport render animation operator was missing part

## [0.1.4] - 2019-12-20
### Added
- Save preset

## [0.1.3] - 2019-11-11
### Added
- Sync View Settings

## [0.1.1] - 2019-09-10
### Added
- Display Log Info (is missing in UI)

## [0.1.0] - 2019-08-28
### Added
- Viewport render & render animation to render menu

## [0.0.9] - 2019-08-21
### Fixed
- Method how menu class is import
- Added proper Prefix & Suffix to menu classes
- Some keymaps not show in Preference panel
- Clearing keymaps

## [0.0.8] - 2019-02-13
### Fixed
- Issue with quick render menu. Now render window will show like as dropdown menu (mentioned by Jacques Lucke)

## [0.0.7] - 2019-01-10
### Changed
- Fixed typo in workspace Texture Paint > was TEXTURE_PAINTING

## [0.0.6] - 2018-12-26
### Changed
- Fix for returning to default Workspace Object Interaction Modes

## [0.0.5] - 2018-12-25
### Added
- Keep Mode stores last Object Interaction Mode and falls back to this instead of Default Workspace Object Interaction Mode

## [0.0.4] - 2018-12-23
### Changed
- Quick render now visible in all screens

## [0.0.3] - 2018-12-23
### Changed
- Order of menu's is set by checking shortcuts
- Icons are now proper workspace icons
- Fixed typo in icon names

## [0.0.2] - 2018-12-22
### Changed
- Merged quick screen switch and quick render menu into one

### Added
- Pie menu and custom position

## [0.0.1] - 2018-12-20
### New
- Initial addon setup
- Renamed all screens to workspace
- Convertion to Blender 2.80

## Notes
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
<!--### Official Rigify Info-->

[0.2.6.7]:https://github.com/schroef/QuickSwitch/releases/tag/v.0.2.6.7
[0.2.6.6]:https://github.com/schroef/QuickSwitch/releases/tag/v.0.2.6.6
[0.2.6.5]:https://github.com/schroef/QuickSwitch/releases/tag/v.0.2.6.5
[0.2.1]:https://github.com/schroef/QuickSwitch/releases/tag/v.0.2.3
[0.2.1]:https://github.com/schroef/QuickSwitch/releases/tag/v.0.2.2
[0.1.1]:https://github.com/schroef/QuickSwitch/releases/tag/v.0.1.1
[0.1.0]:https://github.com/schroef/QuickSwitch/releases/tag/v.0.1.0
[0.0.9]:https://github.com/schroef/QuickSwitch/releases/tag/v.0.0.9
[0.0.8]:https://github.com/schroef/QuickSwitch/releases/tag/v.0.0.8
[0.0.7]:https://github.com/schroef/QuickSwitch/releases/tag/v.0.0.7
[0.0.6]:https://github.com/schroef/QuickSwitch/releases/tag/v.0.0.6
[0.0.5]:https://github.com/schroef/QuickSwitch/releases/tag/v.0.0.5
[0.0.4]:https://github.com/schroef/QuickSwitch/releases/tag/v.0.0.4
[0.0.3]:https://github.com/schroef/QuickSwitch/releases/tag/v.0.0.3
[0.0.2]:https://github.com/schroef/QuickSwitch/releases/tag/v.0.0.2
[0.0.1]:https://github.com/schroef/QuickSwitch/releases/tag/v.0.0.1
