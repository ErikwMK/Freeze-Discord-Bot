Freeze Bot - A Discord Bot for Mario Kart 8 Deluxe to analyse how well you played on different tracks
Author: Erik#8036

This bot is working with a google spreadsheet as 'backend', making it working on any servers.
Requirements:
   - Using Toadbot for wars (Freeze Bot analyses this embeds to get its data)
   - The only use of the toadbot channel should be its commands, becuase else would interfere with the entered amount of wars to be analysed

Different commands: 
   - !setprefix <prefix> Sets the prefix for your server. Default: !
   - !settoadbot <Textchannel> Sets the channel where its analysed
   - !setpermsstats56 Allows everyone/only leaders (manage_members permission) to use following stats56 command

   - !stats <map> <amount of wars> Analyses the stats of the entered map in the amount of entered wars
   - !overallstats <amount of wars> Analyses the stats of every map not seperated in the amount of entered wars
   - !stats56 <amount of wars> Analyses the stats of every map seperated in the amount of wars entered
  <amount of wars> default is None (every war).