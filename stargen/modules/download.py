
from urllib.request import urlopen
from pathlib import Path
from os import listdir
import gzip

from .abs_module import Module

from termcolor import cprint
from interutils import pr, cyan

class Download(Module):
    def __init__(self, stargen):
        super().__init__(stargen, 'down')

    def menu(self) -> tuple:
        return {
            # 'show': (self.show, 'Show downloads'),
            'download': (self.download, 'Download a new wordlists pack from the repo')
        }

    def show(self, args: tuple) -> None:

        if not self.packs:
            return pr('No packs downloaded yet!', '!')
        pr('Available packs:')
        for p in self.packs:
            cprint('  ' + p, 'yellow')
        pr(f'Packs count: ' + cyan(len(self.packs)))

    def download(self, args: tuple) -> None:
        # Identify existing downloads
        try:
            self.packs = listdir(self.dest_dir)
        except FileNotFoundError:
            self.packs = []

        pr(f'Dictionaries repo URL: "{cyan(self.config["dict_url"])}"')
        pr(f'Destination directory: "{cyan(str(self.dest_dir))}"')

        print()
        print("	\r\n	Choose the pack you want to download:\r\n")
        print("     1. Moby         14. french     27. places")
        print("     2. afrikaans    15. german     28. polish")
        print("     3. american     16. hindi      29. random")
        print("     4. aussie       17. hungarian  30. religion")
        print("     5. chinese      18. italian    31. russian")
        print("     6. computer     19. japanese   32. science")
        print("     7. croatian     20. latin      33. spanish")
        print("     8. czech        21. literature 34. swahili")
        print("     9. danish       22. movieTV    35. swedish")
        print("    10. databases    23. music      36. turkish")
        print("    11. dictionaries 24. names      37. yiddish")
        print("    12. dutch        25. net")
        print("    13. finnish      26. norwegian       \r\n")

        # Get user input
        try:
            c = input("Enter number > ")
            if not c:
                return pr('Aborting', '!')
            c = int(c)
            if c > 38 or c < 1:
                pr("Bad choice!", '!')
        except ValueError:
            return pr('Bad choice!', '!')

        # List of files to download:
        pack = (
            (
                "Moby",
                (
                    "mhyph.tar.gz",
                    "mlang.tar.gz",
                    "moby.tar.gz",
                    "mpos.tar.gz",
                    "mpron.tar.gz",
                    "mthes.tar.gz",
                    "mwords.tar.gz",
                ),
            ),
            ("afrikaans", ("afr_dbf.zip",)),
            ("american", ("dic-0294.tar.gz",)),
            ("aussie", ("oz.gz",)),
            ("chinese", ("chinese.gz",)),
            (
                "computer",
                (
                    "Domains.gz",
                    "Dosref.gz",
                    "Ftpsites.gz",
                    "Jargon.gz",
                    "common-passwords.txt.gz",
                    "etc-hosts.gz",
                    "foldoc.gz",
                    "language-list.gz",
                    "unix.gz",
                ),
            ),
            ("croatian", ("croatian.gz",)),
            ("czech", ("czech-wordlist-ascii-cstug-novak.gz",)),
            ("danish", ("danish.words.gz", "dansk.zip")),
            (
                "databases",
                ("acronyms.gz", "att800.gz",
                 "computer-companies.gz", "world_heritage.gz"),
            ),
            (
                "dictionaries",
                (
                    "Antworth.gz",
                    "CRL.words.gz",
                    "Roget.words.gz",
                    "Unabr.dict.gz",
                    "Unix.dict.gz",
                    "englex-dict.gz",
                    "knuth_britsh.gz",
                    "knuth_words.gz",
                    "pocket-dic.gz",
                    "shakesp-glossary.gz",
                    "special.eng.gz",
                    "words-english.gz",
                ),
            ),
            ("dutch", ("words.dutch.gz",)),
            (
                "finnish",
                ("finnish.gz", "firstnames.finnish.gz", "words.finnish.FAQ.gz"),
            ),
            ("french", ("dico.gz",)),
            ("german", ("deutsch.dic.gz", "germanl.gz", "words.german.gz")),
            ("hindi", ("hindu-names.gz",)),
            ("hungarian", ("hungarian.gz",)),
            ("italian", ("words.italian.gz",)),
            ("japanese", ("words.japanese.gz",)),
            ("latin", ("wordlist.aug.gz",)),
            (
                "literature",
                (
                    "LCarrol.gz",
                    "Paradise.Lost.gz",
                    "aeneid.gz",
                    "arthur.gz",
                    "cartoon.gz",
                    "cartoons-olivier.gz",
                    "charlemagne.gz",
                    "fable.gz",
                    "iliad.gz",
                    "myths-legends.gz",
                    "odyssey.gz",
                    "sf.gz",
                    "shakespeare.gz",
                    "tolkien.words.gz",
                ),
            ),
            ("movieTV", ("Movies.gz", "Python.gz", "Trek.gz")),
            (
                "music",
                (
                    "music-classical.gz",
                    "music-country.gz",
                    "music-jazz.gz",
                    "music-other.gz",
                    "music-rock.gz",
                    "music-shows.gz",
                    "rock-groups.gz",
                ),
            ),
            (
                "names",
                (
                    "ASSurnames.gz",
                    "Congress.gz",
                    "Family-Names.gz",
                    "Given-Names.gz",
                    "actor-givenname.gz",
                    "actor-surname.gz",
                    "cis-givenname.gz",
                    "cis-surname.gz",
                    "crl-names.gz",
                    "famous.gz",
                    "fast-names.gz",
                    "female-names-kantr.gz",
                    "female-names.gz",
                    "givennames-ol.gz",
                    "male-names-kantr.gz",
                    "male-names.gz",
                    "movie-characters.gz",
                    "names.french.gz",
                    "names.hp.gz",
                    "other-names.gz",
                    "shakesp-names.gz",
                    "surnames-ol.gz",
                    "surnames.finnish.gz",
                    "usenet-names.gz",
                ),
            ),
            (
                "net",
                (
                    "hosts-txt.gz",
                    "inet-machines.gz",
                    "usenet-loginids.gz",
                    "usenet-machines.gz",
                    "uunet-sites.gz",
                ),
            ),
            ("norwegian", ("words.norwegian.gz",)),
            (
                "places",
                (
                    "Colleges.gz",
                    "US-counties.gz",
                    "World.factbook.gz",
                    "Zipcodes.gz",
                    "places.gz",
                ),
            ),
            ("polish", ("words.polish.gz",)),
            (
                "random",
                (
                    "Ethnologue.gz",
                    "abbr.gz",
                    "chars.gz",
                    "dogs.gz",
                    "drugs.gz",
                    "junk.gz",
                    "numbers.gz",
                    "phrases.gz",
                    "sports.gz",
                    "statistics.gz",
                ),
            ),
            ("religion", ("Koran.gz", "kjbible.gz", "norse.gz")),
            ("russian", ("russian.lst.gz", "russian_words.koi8.gz")),
            (
                "science",
                (
                    "Acr-diagnosis.gz",
                    "Algae.gz",
                    "Bacteria.gz",
                    "Fungi.gz",
                    "Microalgae.gz",
                    "Viruses.gz",
                    "asteroids.gz",
                    "biology.gz",
                    "tech.gz",
                ),
            ),
            ("spanish", ("words.spanish.gz",)),
            ("swahili", ("swahili.gz",)),
            ("swedish", ("words.swedish.gz",)),
            ("turkish", ("turkish.dict.gz",)),
            ("yiddish", ("yiddish.gz",)),
        )[c - 1]

        if pack in self.packs:
            return pr('Pack already downloaded!', '*')

        # Verify destination directory
        dest = Path(self.dest_dir)
        dest.mkdir(exist_ok=True)
        dest = dest / pack[0]
        dest.mkdir(exist_ok=True)

        # Download the files
        for fi in pack[1]:
            pf = pack[0] + "/" + fi
            pr(f"Downloading & ungzipping '{cyan(pf)}'")
            with urlopen(self.config['dict_url'] + pf) as web:
                dest.joinpath(fi.replace('.gz', '')).write_bytes(
                    gzip.decompress(web.read()))

        # Finish
        self.packs.append(pack[0])
        pr("Pack saved to " + str(dest))
        pr("Tip: After downloading wordlists combine them with keywords!", '*')
