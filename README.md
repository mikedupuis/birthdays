# birthdays
Simple docker image to return birthday information

## Getting Started
1. Build the image: `docker build . --tag {tag} --no-cache`
2. Run a container using the image: `docker run --rm -ti --volume=/path/to/volume:/apps/birthdays/data {tag}`

## Setting up the data

Sample data file to be stored in the mounted directory:

```
{
    "people": [
        {
            "name": "Barack Obama",
            "gender": "male",
            "birthday": {
                "year": 1961,
                "month": 8,
                "day": 4
            }
        },
        "birthday-alerts": {
            "alert-threshold-days": 7
        }
    ]
}
```

### Notes
#### Sample output
`Barack Obama's birthday is in 199 days and he will be 59 years old`

#### Person data
1. `Person.gender` field is optional. Including it will cause the script to use gendered pronouns (i.e. "he" and "she"). Omitting it will cause the script to use the non-gendered pronoun ("they"). Only applicable when `Person.birthday.year` is included.
2. `Person.birthday.year` is optional Including it will cause the script to announce the number of years old they will be on their upcoming birthday.

#### birthday-alerts
Birthday alerts will cause messages to be written to `stdout` when a birthday is upcoming within `birthday-alerts.alert-threshold-days` days.
