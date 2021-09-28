# Guild Scaffolding

Creates Discord guild categories, channels, and roles automatically based on structured data.

For each category, a channel category will be created, a helper role will be created for the category, and a voice channel will be added to the category.

Then, for each item in the category, a channel and role will be created. This role, the helper role for the category, as well as every role in roles_to_add_to_all, will have view access to the channel. @everyone will not be able to view the channel.

Take care to make sure that you will not reach the role/channel limit. Your guild will look very weird if the bot fails halfway through due to such limits.

## Why?

This allows for you to have one Discord guild with a large number of channels, where users can choose which channels/categories they want to see. One example of this is a study group, where many topics are covered, but you might only want to see a few.

## Usage

```bash
pipenv sync
pipenv run python main.py
```

Works best with an autorole bot such as YAGPDB.
