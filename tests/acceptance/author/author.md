# Prerequisites
Add your discord id to the `AUTHOR_IDS` variable of the `.env` file as described in the [Readme](../../../README.md#env)

# Test
`!_author <id>` Allows the developer to test any of the functionalities as if they were using another discord account with the chosen \<id\>

The developer needs just prepend `!_author <id>` to any of the commands they wish to execute.
Example
\>
```
!_author 1 !add_name John Doe
```

\<
```
Command executed as 1:
Name added
```

As of yet, not all functions work such that Discord mentions can be replaced by debug id mentions (for example, \<@1\>)
