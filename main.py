#!/usr/bin/env python3

import curses
from client import *

def main(stdscr):
    k = 0 #Last pressed key
    index = 0 #List index
    mode = 'Subscriptions'

    # Init colours
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.noecho()
    curses.curs_set(0) #Make cursor invisible

    stdscr.clear()
    stdscr.addstr(0, 0, 'Loading subscriptions...')
    stdscr.refresh()

    videos = load_subscriptions_videos()

    #Loop until 'q' is pressed
    while (k != ord('q')):
        h, w = stdscr.getmaxyx() #Get height and width
        h_w = int(w / 2) #Half width

        col_r = curses.newpad(h, h_w) #Init right column

        #Controlls
        if (k == curses.KEY_DOWN or k == ord('j')) and index < len(videos) - 1:
            index += 1
        elif (k == curses.KEY_UP or k == ord('k')) and index > 0:
            index -= 1
        elif k == ord('h'):
            help_str = "'k/j' - Up/Down\n'Enter' - Play video\n'F1' - Load subscription videos\n'F2' - Search\n'F3' - Show video info\n'F4' - Load related videos\n'F5' - More videos from this channel\n'F6' - Subscribe\n'h' - Help\n'q' - Quit"
            col_r.addstr(5, 0, help_str)
        elif k == 10:
            os.system('nohup mpv --msg-level=all=warn,ao/alsa=error https://youtu.be/' + videos[index].id + ' > ' + path + '/mpv.log &')
            col_r.attron(curses.color_pair(2))
            col_r.addstr(4, 0, 'Now playing')
            col_r.attroff(curses.color_pair(2))
        elif k == 265:
            mode = 'Subscriptions'
            index = 0
            stdscr.addstr(0, 0, 'Loading subscriptions...')
            stdscr.refresh()
            videos = load_subscriptions_videos()
        elif k == 266:
            index = 0
            stdscr.addstr(0, 0, 'Enter search query:')
            curses.echo()
            query = stdscr.getstr(1,0, h_w)
            mode = 'Search results for: ' + query.decode('utf-8')
            curses.noecho()
            stdscr.addstr(0, 0, 'Loading videos...  ')
            stdscr.refresh()
            videos = search_videos(query)[::-1]
        elif k == 267:
            col_r.addstr(4, 0, 'Loading video info...')
            col_r.refresh(4, 0, 4, h_w, h - 2, w)
            try:
                col_r.addstr(4, 0, get_video_info(videos[index].id))
            except:
                pass
        elif k == 268:
            mode = 'Related'
            index = 0
            stdscr.addstr(0, 0, 'Loading related videos...')
            stdscr.refresh()
            videos = get_related_videos(videos[index].id)
        elif k == 269:
            mode = 'Channel: ' + videos[index].channel_name
            stdscr.addstr(0, 0, 'Loading videos from channel...')
            stdscr.refresh()
            videos = get_videos_from_channel(videos[index].channel_id)
            index = 0
        elif k == 270:
            if not toggle_subscription(videos[index].channel_id):
                col_r.attron(curses.color_pair(1))
                col_r.addstr(3, 0, 'Unsubscibed')
                col_r.attroff(curses.color_pair(1))

        col_l = curses.newpad(len(videos) + 1, h_w) #Init left column

        #Render middle border
        for y in range(1, h - 1):
            stdscr.addstr(y, h_w - 1, '|')

        #Render status bar
        status_str = 'Videos: ' + str(len(videos)) + ' Current: ' + str(index + 1) + ' || ' + mode + " || Press 'h' for help "
        if len(status_str) < w:
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(h - 1, 0, status_str)
            stdscr.addstr(h - 1, len(status_str), " " * (w - len(status_str) - 1)) #Fill up space
            stdscr.attroff(curses.color_pair(3))

        if videos and w >= 32:
            #Render videos list
            for i in range(0, len(videos)):
                col_l.addstr(i, 0, videos[i].title)

            #Print video info
            stdscr.addstr(0, h_w - 1, '>')
            col_r.addstr(0, 0, videos[index].title)
            col_r.addstr(1, 0, videos[index].channel_name)
            col_r.addstr(2, 0, str(videos[index].upload_date))
            if is_subscribed(videos[index].channel_id):
                col_r.attron(curses.color_pair(1))
                col_r.addstr(3, 0, 'Subscribed')
                col_r.attroff(curses.color_pair(1))
        else:
            col_l.addstr(0, 0, 'No results')



        # Refresh
        try:
            stdscr.refresh()
            col_l.refresh(index, 0, 0, 0, h - 2, h_w - 2)
            col_r.refresh(0, 0, 0, h_w, h - 2, w)
        except:
            pass

        # Wait for next input
        k = stdscr.getch()

        stdscr.clear()

curses.wrapper(main)
