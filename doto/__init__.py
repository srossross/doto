from __future__ import print_function, division, absolute_import
import requests
import pandas as pd

from doto.logger import log
from doto.config import Config
from doto.droplet import Droplet
from doto.d0_mixin import d0mixin

BASEURL = "https://api.digitalocean.com"

class connect_d0(d0mixin, object):

    def __init__(self, path=None):
        config = Config(path)
        self._client_id = config.get('Credentials','client_id')
        self._api_key = config.get('Credentials','api_key')

    def __str__(self):
        return "DigitialOcean Connection Object"

    def __repr__(self):
        return "D0:Connected"


    def create_droplet(self,name=None,size_id=None,image_id=None,
                       region_id=None,ssh_key_ids=None,private_networking=None):
        """
        Creates a droplet

        :type name: string
        :param name: The NAME of the droplet (name will be used as a reference
        on D0's servers)

        :type size_id: int
        :param size_id: The ID corresponding to requested size of the image (see
        connect_d0.get_sizes)

        :type image_id: int
        :param image_id: The ID corresponding to the requested image (see
        connect_d0.images)

        :type region_id: int
        :param region_id: The ID corresponding to the requested region (see
        connect_d0.region_id)

        :type ssh_key_ids: int
        :param ssh_key_ids: An optional list of comma separated IDs corresponding
        to the requested ssh_keys to be added to the server
        (see connect_d0.get_ssh_keys)

        :type private_networking: int
        :param private_networking: An optional bool which enables a private network interface
        if the region supports private networking

        droplet = d0.create_droplet(name='Random',
                               size_id=66, #512MB
                               image_id=1341147, #Docker 0.7 Ubuntu 13.04 x64
                               region_id=1, #New York
                               ssh_key_ids=18669
                               )
        """

        data = self._request("/droplets/new",name=name,
                          size_id=size_id,image_id=image_id,
                          region_id=region_id,ssh_key_ids=ssh_key_ids,
                          private_networking=private_networking)

        #don't like this but will do for now
        data['droplet']['_client_id'] = self._client_id
        data['droplet']['_api_key'] = self._api_key

        return Droplet(**data['droplet'])
        # https://api.digitalocean.com/droplets/new?client_id=[your_client_id]&api_key=[your_api_key]&
        # name=[droplet_name]&size_id=[size_id]&image_id=[image_id]&region_id=[region_id]&ssh_key_ids=
        # [ssh_key_id1],[ssh_key_id2]




    def get_all_droplets(self, status_check=None):
        # https://api.digitalocean.com/droplets/?client_id=[your_client_id]&api_key=[your_api_key]
        log.info("Get All Droplets")
        data = self._request("/droplets",status_check)

        if status_check:
            return data

        #don't like this but will do for now
        for drop in data['droplets']:
            #convert dictionary to droplet objects
            drop['_client_id'] = self._client_id
            drop['_api_key'] = self._api_key


        #convert dictionary to droplet objects
        return [Droplet(**drop) for drop in data['droplets']]

    def get_droplet(self, id=None):
        # https://api.digitalocean.com/droplets/[droplet_id]?client_id=[your_client_id]&api_key=[your_api_key]
        data = self._request("/droplets/"+str(id))

        #don't like this but will do for now
        data['droplet']['_client_id'] = self._client_id
        data['droplet']['_api_key'] = self._api_key

        #convert dictionary to droplet objects
        return Droplet(**data['droplet'])


    def get_sizes(self, status_check=None):
        # https://api.digitalocean.com/sizes/?client_id=[your_client_id]&api_key=[your_api_key]

        data = self._request("/sizes", status_check)

        if status_check:
            return data

        df = pd.DataFrame.from_dict(data['sizes'])
        df.sort(['cost_per_hour'],inplace=True)
        return df


    def get_regions(self,status_check=None):
        # https://api.digitalocean.com/sizes/?client_id=[your_client_id]&api_key=[your_api_key]

        data = self._request("/regions", status_check)

        if status_check:
            return data

        df = pd.DataFrame.from_dict(data['regions'])
        return df

    def get_images(self, status_check=None):
        """
        Convenience method to get Digital Ocean's list of public images
        and users current private images

        Data is converted to a Pandas's data frame for easy reading and sorting
        https://api.digitalocean.com/sizes/?client_id=[your_client_id]&api_key=[your_api_key]

        >>> df_imgs = d0.get_images()
        >>> print df_imgs.head()

        or sort the images based on the distribution
        >>> df_imgs.sort('distribution',inplace=True)
        >>> df_imgs.head()
        """

        # https://api.digitalocean.com/images/?client_id=[your_client_id]&api_key=[your_api_key]

        data = self._request("/images", status_check)

        if status_check:
            return data

        df = pd.DataFrame.from_dict(data['images'])
        return df



    def get_ssh_keys(self, status_check=None):
        """
        Convenience method to get user's ssh key ids

        Data is converted to a Pandas's data frame for easy reading and sorting
        https://api.digitalocean.com/ssh_keys/?client_id=[your_client_id]&api_key=[your_api_key]

        >>> df_keys = d0.get_ssh_keys()
        >>> print df_keys.head()

        """


        data = self._request("/ssh_keys", status_check)

        if status_check:
            return data

        df = pd.DataFrame.from_dict(data['ssh_keys'])
        return df



    def get_domains(self, status_check=None):
        """
        Convenience method to get Digital Ocean's list of Domains

        Data is converted to a Pandas's data frame for easy reading and sorting
        https://api.digitalocean.com/domains/?client_id=[your_client_id]&api_key=[your_api_key]

        >>> df_domains = d0.get_ssh_keys()
        >>> print df_domains.head()

        """


        data = self._request("/domains", status_check)

        if status_check:
            return data

        df = pd.DataFrame.from_dict(data['domains'])
        return df








