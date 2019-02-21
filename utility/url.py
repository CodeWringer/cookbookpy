def get_url(source_path, dest_path):
        """Returns a relative url, based on the given file paths.
        Parameters
        ---------
        source_path : str
          The full file path to start the url from.
        dest_path : str
          The full file path to end the url at.
        """
        replace_source = source_path.replace('\\', '/')
        replace_dest = dest_path.replace('\\', '/')

        splits_source = replace_source.split('/')
        splits_dest = replace_dest.split('/')
        splits_root = []

        count_source = len(splits_source)
        count_dest = len(splits_dest)
        count = min(count_source, count_dest)

        # Find common url.
        for i in range(0, count):
            split_source = splits_source[i]
            split_dest = splits_dest[i]
            if (split_source == split_dest):
                splits_root.append(split_source)
            else:
                break

        count_root = len(splits_root)
        url = ''

        # Walk back to root.
        for i in range(count_root, count_source - 1):
            url += '../'

        # Walk forward to goal.
        for i in range(count_root, count_dest - 1):
            url += '%s/' % (splits_dest[i])

        url += splits_dest[count_dest - 1]

        return url
