#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 12:32:53 2017

@author: wroscoe
"""
import os
import time
import json
import random

import numpy as np
import pandas as pd
from PIL import Image

from source import util


class Tub(object):
    """
    A datastore to store sensor data in a key, value format.

    Accepts str, int, float, image_array, image, and array data types.

    For example:

    #Create a tub to store speed values.
    >>> path = '~/mydonkey/test_tub'
    >>> inputs = ['user/speed', 'cam/image']
    >>> types = ['float', 'image']
    >>> t=Tub(path=path, inputs=inputs, types=types)

    """

    def __init__(self, path, inputs=None, types=None):

        self.path = os.path.expanduser(path)
        self.meta_path = os.path.join(self.path, 'meta.json')
        self.df = None

        exists = os.path.exists(self.path)

        if exists:
            # load log and meta
            with open(self.meta_path, 'r') as f:
                self.meta = json.load(f)
            self.current_ix = self.get_last_index() + 1

        elif not exists and inputs:
            # create log and save meta
            os.makedirs(self.path)
            self.meta = {'inputs': inputs, 'types': types}
            with open(self.meta_path, 'w') as f:
                json.dump(self.meta, f)
            self.current_ix = 0
        else:
            msg = "The tub path you provided doesn't exist and you didn't pass any meta info (inputs & types)" + \
                  "to create a new tub. Please check your tub path or provide meta info to create a new tub."

            raise AttributeError(msg)

        self.start_time = time.time()

    def get_last_index(self):
        index = self.get_index()
        if len(index) >= 1:
            return max(index)
        return -1

    def update_df(self):
        df = pd.DataFrame([self.get_json_record(i) for i in self.get_index(shuffled=False)])
        self.df = df

    def get_df(self):
        if self.df is None:
            self.update_df()
        return self.df

    def get_index(self, shuffled=True):
        files = next(os.walk(self.path))[2]
        record_files = [f for f in files if f[:6] == 'record']

        def get_file_index(file_name):
            try:
                name = file_name.split('.')[0]
                num = int(name.split('_')[1])
            except:
                num = 0
            return num

        nums = [get_file_index(f) for f in record_files]

        if shuffled:
            random.shuffle(nums)
        else:
            nums = sorted(nums)

        return nums

    @property
    def inputs(self):
        return list(self.meta['inputs'])

    @property
    def types(self):
        return list(self.meta['types'])

    def get_input_type(self, key):
        input_types = dict(zip(self.inputs, self.types))
        return input_types.get(key)

    def write_json_record(self, json_data):
        path = self.get_json_record_path(self.current_ix)
        try:
            with open(path, 'w') as fp:
                json.dump(json_data, fp)
        except:
            raise

    def get_num_records(self):
        import glob
        files = glob.glob(os.path.join(self.path, 'record_*.json'))
        return len(files)

    def make_record_paths_absolute(self, record_dict):
        d = {}
        for k, v in record_dict.items():
            if type(v) == str:  # filename
                if '.' in v:
                    v = os.path.join(self.path, v)
            d[k] = v

        return d

    def remove_record(self, ix):
        """
        remove data associate with a record
        """
        record = self.get_json_record_path(ix)
        os.unlink(record)

    def put_record(self, data):
        """
        Save values like images that can't be saved in the csv log and
        return a record with references to the saved values that can
        be saved in a csv.
        """
        json_data = {}

        for key, val in data.items():
            typ = self.get_input_type(key)

            if typ in ['str', 'float', 'int', 'boolean']:
                json_data[key] = val

            elif typ is 'image':
                name = self.make_file_name(key, ext='.jpg')
                val.save(os.path.join(self.path, name))
                json_data[key] = name

            elif typ == 'image_array':
                img = Image.fromarray(np.uint8(val))
                name = self.make_file_name(key, ext='.jpg')
                img.save(os.path.join(self.path, name))
                json_data[key] = name

            else:
                msg = 'Tub does not know what to do with this type {}'.format(typ)
                raise TypeError(msg)

        self.write_json_record(json_data)
        self.current_ix += 1
        return self.current_ix

    def get_json_record_path(self, ix):
        # fill zeros
        # return os.path.join(self.path, 'record_'+str(ix).zfill(6)+'.json')
        # don't fill zeros
        return os.path.join(self.path, 'record_' + str(ix) + '.json')

    def get_json_record(self, ix):
        path = self.get_json_record_path(ix)
        try:
            with open(path, 'r') as fp:
                json_data = json.load(fp)
        except UnicodeDecodeError:
            raise Exception('bad record: %d. You may want to run `python manage.py check --fix`' % ix)
        except:
            raise

        record_dict = self.make_record_paths_absolute(json_data)
        return record_dict

    def get_record(self, ix):
        json_data = self.get_json_record(ix)
        data = self.read_record(json_data)
        return data

    def read_record(self, record_dict):
        data = {}
        for key, val in record_dict.items():
            typ = self.get_input_type(key)

            # load objects that were saved as separate files
            if typ == 'image_array':
                img = Image.open((val))
                val = np.array(img)

            data[key] = val
        return data

    def make_file_name(self, key, ext='.png'):
        name = '_'.join([str(self.current_ix), key, ext])  # don't fill zeros
        name = name.replace('/', '-')
        return name

    def shutdown(self):
        """ Required by the Part interface """
        pass

    def get_record_gen(self, record_transform=None, shuffle=True, df=None):
        """
        Returns records.

        Parameters
        ----------
        record_transform : function
            The mapping function should handle records in dict format
        shuffle : bool
            Shuffle records
        df : numpy Dataframe
            If df is specified, the generator will use the records specified in that DataFrame. If None,
            the internal DataFrame will be used by calling get_df()

        Returns
        -------
        A dict with keys mapping to the specified keys, and values lists of size batch_size.

        See Also
        --------
        get_df
        """
        if df is None:
            df = self.get_df()

        while True:
            for _ in self.df.iterrows():
                if shuffle:
                    record_dict = df.sample(n=1).to_dict(orient='record')[0]

                record_dict = self.read_record(record_dict)

                if record_transform:
                    record_dict = record_transform(record_dict)

                yield record_dict

    def get_batch_gen(self, keys=None, batch_size=128, record_transform=None, shuffle=True, df=None):
        """
        Returns batches of records.

        Additionally, each record in a batch is split up into a dict with inputs:list of values. By specifying keys as a subset of the inputs, you can filter out unnecessary data.

        Parameters
        ----------
        keys : list of strings
            List of keys to filter out. If None, all inputs are included.
        batch_size : int
            The number of records in one batch.

        Returns
        -------
        A dict with keys mapping to the specified keys, and values lists of size batch_size.

        See Also
        --------
        get_record_gen
        """
        record_gen = self.get_record_gen(record_transform=record_transform, shuffle=shuffle, df=df)

        if df is None:
            df = self.get_df()

        if keys is None:
            keys = list(self.df.columns)

        while True:
            record_list = [ next(record_gen) for _ in range(batch_size) ]

            batch_arrays = {}
            for i, k in enumerate(keys):
                arr = np.array([r[k] for r in record_list])
                batch_arrays[k] = arr
            yield batch_arrays

    def get_train_gen(self, X_keys, Y_keys, batch_size=128, record_transform=None, df=None):
        """
        Returns a training/validation set.

        The records are always shuffled.

        Parameters
        ----------
        X_keys : list of strings
            List of the feature(s) to use. Must be included in Tub.inputs.
        Y_keys : list of strings
            List of the label(s) to use. Must be included in Tub.inputs.

        Returns
        -------
        A tuple (X, Y), where X is a two dimensional array ( len(X_keys) x batch_size ) and Y is a two dimensional array ( len(Y_keys) x batch_size ).

        See Also
        --------
        get_batch_gen
        """
        batch_gen = self.get_batch_gen(X_keys + Y_keys, batch_size=batch_size, record_transform=record_transform, df=df)

        while True:
            batch = next(batch_gen)
            X = [batch[k] for k in X_keys]
            Y = [batch[k] for k in Y_keys]
            yield X, Y

    def get_train_val_gen(self, X_keys, Y_keys, batch_size=128, train_frac=.8,
                          train_record_transform=None, val_record_transform=None):
        """
        Create generators for training and validation set.

        Parameters
        ----------
        train_frac : float
            Training/validation set split.
        train_record_transform : function
            Transform function for the training set. Used internally by Tub.get_record_gen().
        val_record_transform : function
            Transform  function for the validation set. Used internally by Tub.get_record_gen().

        Returns
        -------
        A tuple (train_gen, val_gen), where where train_gen is the training set generator, and
        val_gen the validation set generator.

        See Also
        --------
        get_train_gen
        get_record_gen
        """
        if self.df is None:
            self.update_df()

        train_df = self.df.sample(frac=train_frac, random_state=200)
        val_df = self.df.drop(train_df.index)

        train_gen = self.get_train_gen(X_keys=X_keys, Y_keys=Y_keys, batch_size=batch_size,
                                       record_transform=train_record_transform, df=train_df)

        val_gen = self.get_train_gen(X_keys=X_keys, Y_keys=Y_keys, batch_size=batch_size,
                                     record_transform=val_record_transform, df=val_df)

        return train_gen, val_gen


class TubWriter(Tub):
    def __init__(self, *args, **kwargs):
        super(TubWriter, self).__init__(*args, **kwargs)

    def run(self, *args):
        """
        Accepts values, pairs them with their input keys and saves them
        to disk.
        """
        assert len(self.inputs) == len(args)
        record = dict(zip(self.inputs, args))
        self.put_record(record)


class TubReader(Tub):
    def __init__(self, *args, **kwargs):
        super(TubReader, self).__init__(*args, **kwargs)
        self.read_ix = 0

    def run(self, *args):
        """
        Accepts keys to read from the tub and retrieves them sequentially.
        """
        if self.read_ix >= self.current_ix:
            return None

        record_dict = self.get_record(self.read_ix)
        self.read_ix += 1
        record = [record_dict[key] for key in args ]
        return record


class TubGroup(Tub):
    def __init__(self, tub_paths_arg):
        tub_paths = util.files.expand_path_arg(tub_paths_arg)
        self.tubs = [Tub(path) for path in tub_paths]
        self.input_types = {}

        record_count = 0
        for t in self.tubs:
            t.update_df()
            record_count += len(t.df)
            self.input_types.update(dict(zip(t.inputs, t.types)))

        self.meta = {'inputs': list(self.input_types.keys()),
                     'types': list(self.input_types.values())}

        self.df = pd.concat([t.df for t in self.tubs], axis=0, join='inner')

    @property
    def inputs(self):
        return list(self.meta['inputs'])

    @property
    def types(self):
        return list(self.meta['types'])

    def get_num_tubs(self):
        return len(self.tubs)

    def get_num_records(self):
        return len(self.df)
