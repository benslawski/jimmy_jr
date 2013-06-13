from spynner import *
import json

class LookupInterface:

    def __init__(self):
        pass

    def getGame(self, home, vis, date, num):
        lookup = 'http://mlb.mlb.com/mlb/gameday/index.jsp?' \
               + 'gid=' + date + '_' \
               + vis + 'mlb_' \
               + home + 'mlb_' \
               + str(num) \
               + '&mode=plays'

        browser = Browser()
        raw_data = browser.download(lookup)
        data = self.parseGame(raw_data)

        browser.close()
        return data


    def parseGame(self, game_data):
        parsed_data = []

        innings = game_data.split('<li class="plays-half-inning">')[1:]
        for inning in innings:
            inning_data = []
            atbats = re.split('<dl class="plays-.*-description">', inning)[1:]
            for playline in atbats:
                play = playline.split('</dl>')[0]
                if '</span>' in play:
                    play_type = 'AtBat'
                    play = play.split('</span>')[1]
                else:
                    play_type = 'Action'
                    play = play.split('<dt>')[1]
                play = play.split('</dt>')[0]
                inning_data.append([play_type, play.strip()])
            parsed_data.append(inning_data)

        return parsed_data


if __name__ == "__main__":
    DEADLIST = [ \
                   'cle_cha_2012_04_10.dat', \
                   'bos_nya_2012_04_22.dat', \
                   'was_mia_2012_04_22.dat', \
                   'pit_col_2012_04_23.dat', \
                   'col_hou_2012_05_29.dat', \
                   'ari_col_2012_06_07.dat', \
                   'oak_tex_2012_07_16.dat', \
                   'ari_mia_2012_08_23.dat', \
                   'was_lan_2012_09_18.dat', \
                   'nya_tor_2012_09_18.dat', \
                   'nyn_phi_2012_09_18.dat', \
                   'mia_nyn_2011_04_01.dat', \
                   'mia_nyn_2011_04_02.dat', \
                   'mia_nyn_2011_04_03.dat', \
                   'pit_mil_2011_04_12.dat', \
                   'bos_tba_2011_04_13.dat', \
                   'phi_flo_2011_04_16.dat', \
                   'was_mil_2011_04_16.dat', \
                   'chn_sdn_2011_04_19.dat', \
                   'pit_was_2011_04_22.dat', \
                   'min_tba_2011_04_26.dat', \
                   'cin_hou_2011_05_02.dat', \
                   'col_nyn_2011_05_11.dat', \
                   'chn_sfn_2011_05_15.dat', \
                   'det_kca_2011_05_15.dat', \
                   'was_pit_2011_05_17.dat', \
                   'nyn_flo_2011_05_17.dat', \
                   'xxx_xxx_2011_07_12.dat', \
                   'phi_was_2011_08_14.dat', \
                   'nya_tba_2011_08_14.dat', \
                   'det_min_2011_08_16.dat', \
                   'flo_cin_2011_08_25.dat', \
                   'nyn_atl_2011_08_27.dat', \
                   'bal_nya_2011_08_27.dat', \
                   'nyn_atl_2011_08_28.dat', \
                   'bos_oak_2011_08_28.dat', \
                   'phi_flo_2011_08_28.dat', \
                   'was_lan_2011_09_07.dat', \
                   'chn_mil_2013_04_10.dat', \
                   'bos_tba_2013_04_12.dat', \
                   'min_nyn_2013_04_14.dat', \
                   'col_nyn_2013_04_15.dat', \
                   'chn_tex_2013_04_17.dat', \
                   'col_nyn_2013_04_17.dat', \
                   'bos_kca_2013_04_19.dat', \
                   'cha_min_2013_04_19.dat', \
                   'min_mia_2013_04_22.dat', \
                   'col_atl_2013_04_22.dat', \
                   'cha_cle_2013_04_23.dat', \
                   'kca_cha_2013_05_03.dat', \
                   'atl_nyn_2013_05_04.dat', \
                   'was_det_2013_05_07.dat', \
                   'oak_tex_2013_05_14.dat', \
               ]

    YEAR = '2013'
    schedule = open('data/schedules/' + YEAR + '.dat', 'r').readlines()
    outpath = 'data/clean/'

    for game in schedule:
        tester = LookupInterface()
        splitgame = game.split(',')

        year = splitgame[1]

        month = splitgame[2]
        if len(month) == 1:
            month = '0' + month

        day = splitgame[3]
        if len(day) == 1:
            day = '0' + day

        names = {
                    'stl':'sln',
                    'sd':'sdn',
                    'sf':'sfn',
                    'kc':'kca',
                    'tb':'tba',
                    'laa':'ana',
                    'fla':'mia',
                    'nym':'nyn',
                    'nyy':'nya',
                    'chc':'chn',
                    'cws':'cha',
                    'lad':'lan',
                }

        home = splitgame[5].strip().lower()
        if home in names:
            home = names[home]
        vis = splitgame[4].strip().lower()
        if vis in names:
            vis = names[vis]

        filename = '_'.join([home, vis, year, month, day]) + '.dat'
        if filename in DEADLIST:
            continue
        try:
            open(outpath + filename, 'r')
            continue
        except:
            print filename
            pass

        try:
            results = tester.getGame(home, vis, '_'.join([year, month, day]), 1)
        except Exception as e:
            print '\t', type(e), e.message

        if not results:
            print '\t', filename
            continue

        results = json.dumps({'home':home, 'vis':vis, 'plays':results, 'date':'_'.join([year, month, day])})

        outfile = open(outpath + filename, 'w')
        outfile.write(results)
        outfile.close()

