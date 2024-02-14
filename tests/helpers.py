from shade import ShadeLocal
import time
from typing import List, Union
from pathlib import Path
from shade.v1.models import AssetModel, Job, JobState
from shade.v1.api import APIException


# Wooo these can all be fixtures
def wait_for_assets(backend: ShadeLocal, paths: List[Path], timeout: int = 30) -> List[AssetModel]:
    """Wait for assets to be indexed"""
    start_time = time.time()
    while time.time() < start_time + timeout:
        try:
            # Make sure they're all there
            return [backend.assets.get_asset_by_path(asset) for asset in paths]
        except APIException as e:
            if e.status_code != 404:
                raise e
        time.sleep(1)
    raise Exception(f"Timed out waiting for assets to index: {paths}")


def wait_for_jobs(
        backend: ShadeLocal,
        jobs: List[Job],
        handles: List[Union[Path, AssetModel]],
        timeout: int = 30
) -> List[AssetModel]:
    """Wait for jobs to run on assets"""

    # each handle can be a path or an asset
    paths = [handle.path if isinstance(handle, AssetModel) else handle for handle in handles]

    start_time = time.time()
    done = False

    while not done and time.time() < start_time + timeout:
        done = True
        assets = wait_for_assets(backend, paths, timeout)
        for asset in assets:
            # if at least one job is not done, try again
            if any(getattr(asset, job) not in (JobState.COMPLETED, JobState.FAILED) for job in jobs):
                print(f"Waiting for {asset.path} to finish indexing")
                done = False
                break
            elif getattr(asset, 'preview_job_state') == JobState.FAILED:
                print(f"Previews failed so theres no point in waiting on {asset.path}")
                done = True
                break

            # no need to check the rest of the assets we found at least one unfinished job
            if not done:
                break

        # wait before checking again
        if not done:
            time.sleep(1)

    if not done:
        raise Exception(f"Timed out waiting for jobs to complete: {jobs} on assets: {paths}")

    return assets
