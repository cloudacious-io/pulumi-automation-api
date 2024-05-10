# Pulumi Automation API
Create infrastructure from code using the Pulumi Automation API.
## Deployment
1. Build the container from the Dockerfile
```
docker build -t pulumi-automation-api . --progress=plain
```
Note: adding the `--no-cache` option can be helpful to force a complete rebuild.

2. Run the container
```
docker run --rm -it --name pulumi-automation-api --volume $(pwd)/:/code -v /var/run/docker.sock:/var/run/docker.sock pulumi-automation-api bash
```
The volume including `docker.sock` enables the container to build another container, assuming you are using Docker. Note that this may not work on Windows, it is only tested in Linux (use WSL!).

3. Fill out the `.env` file.
```
(instructions to come)
```
4. Create your `stack_info`
```
(instructions to come)
```
5. Run 
```
(instructions to come)
```
## Support
Come hang out with us in our [Discord](https://discord.gg/d7YccKnenh)! Or if that link isn't working (Discord links are prone to breaking), look for the latest at [cloudacious.io](https://cloudacious.io).

## Roadmap
...

## Contributing
Help is welcome! Please submit an issue with your suggestion to get started.

## Authors and acknowledgment
Authored by [@surfingdoggo](https://gitlab.com/SurfingDoggo).

## License
TBD

## Project status
Actively maintained as of April 2024, and open to contributions!
