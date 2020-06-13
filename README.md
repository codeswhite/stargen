## Interactive wordlists generator

### TODO:

- add more download sources
- improve config
- add more keyword expansion modifiers

- Rewrite Concept: this can be applied to slain as well

- Implement multi-base generation based on the following info:
  -  Stage 1:    Collect, capitalize and extend to aquire a *set* of keywords
  - Stage 2:    Create a *set* of required crunches to be made in order to fill with the desired min-max len    Note the various keywords lengths, espacially the longest and shortest keywords
  -  Stage 3:    Crunch some
  - Stage 4:    Begin creation of one big happy dict
    Schema "Rake":        kwrds: list[Keyword]        min_len: int        max_len: int        charset: str    Schema "Keyword"(str):        keyword: str        _length: len(self.keyword)        required_crunch: ???
