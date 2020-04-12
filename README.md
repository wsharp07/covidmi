# covidmi
[![CircleCI](https://circleci.com/gh/wsharp07/covidmi.svg?style=svg)](https://circleci.com/gh/wsharp07/covidmi)

An app that scrapes the county COVID-19 information for Michigan and stores it in a database

## Getting Started

### Prerequites

This project uses Azure SQL Database.

### Setting up the Environment

This project uses dotenv files.

1. Create a `.env` file in the root folder
2. Add the following parameters with appropriate values

```
SQL_DATABASE=
SQL_HOSTNAME=
SQL_USERNAME=
SQL_PASSWORD=
```