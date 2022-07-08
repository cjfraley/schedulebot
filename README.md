# schedulebot

# MVP
1. Get currently due tasks
2. Take current number of poms
3. In order of priority, fill time for today.
4. Snooze everything else non-short break

## Next
5. Run data collection
6. Make list of labelling things

# Get away from docker possible
*https://www.containiq.com/post/docker-alternatives
*https://www.redhat.com/sysadmin/run-podman-windows
*https://dsstream.com/using-kubernetes-without-docker-what-do-you-need-to-know/
*https://dsstream.com/using-kubernetes-without-docker-what-do-you-need-to-know/


# Old Notes: Todoist Helper
A Django WebApp adding some functionality for my workflow using todoist

# DoToday Helper
What do I do today?
My approach to using todoist is to record everything and then decide what to do from there. It would be helpful to have an easy way to quickly remove and reschedule what I can ignore.

## Currently what it does:
Goes through tasks in descending priority order and grabs ones that either have no time estimate or include a time estimate that does not surpass (cumulatively) an amount of time I have to spend (currently set at 4 poms)

## Todo
1. Allow for interactivity
  1. Change amount of time I estimate having
  1. https://stackoverflow.com/questions/32542192/checkbox-change-update-html-with-current-checked-elements
1. Change workflow so that p1s are never delayed
1. Allow filtering based on todoist queries
1. Bring up stuff on margins in interactive form
  1. ~p1s should they get bumped down?~
  1. Select what does and doesn't get delayed from margin
1. Autodelay relevant stuff
1. Pretty up the interface

# Data tracking
Track some metrics and put them in a form that's useful

## Currently what it does:
Grabs last 24 hrs of delay and mark done and sends it to google drive on running script

## Todo
1. Automate data collection
  1. Make data collection a google function
  2. Move data storage to database
2. explore what metrics are useful and think about that stuff

# General Todo
1. CI/CD
1. Make data refresh up to last refresh or limit

1. Add draggable tasks
  - https://stackoverflow.com/questions/31116519/drag-and-drop-table-moving-cells-to-different-columns
  - https://htmldom.dev/drag-and-drop-table-column/
  - https://www.w3schools.com/howto/howto_css_two_columns.asp
1. Add more info to task tiles
1. Auto add repo todos to todoist on commit
1. todoist link to html link conversion
1. Nest subtasks/projects
2. Generalize for other users
1. Make it pretty
  - https://www.w3schools.com/css/css_max-width.asp
  - https://stackoverflow.com/questions/51445637/css-border-outline-with-outside-padding
