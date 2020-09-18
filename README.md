# Adamah #
Library and helpers for working with API of www.adamah.at

## Configuration ##
Add `settings.json` to `/config`, see `/config/settings.sample.json` for reference.

## Functions ##
### Check for available details on upcoming box ###
```bash
python3 check_deliveries.py
```
Checks for upcoming boxes having content available. Sends notification emails to the recipients configured in `settings.json`.

## docker support ##
A Dockerfile is included to allow to package these helpers into a docker image. Use the common methods `docker build`, `docker tag`, and `docker push`.

The container will not run permanently but should be invoked to trigger a specific script.

e.g.:
```bash
docker exec -d [container] python3 check_deliveries.py
```