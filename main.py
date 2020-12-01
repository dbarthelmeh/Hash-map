class Tombstone:
    """Holds the spot of deleted entries.  Prevents unwanted errors during
     lookup."""
    def __init__(self):
        pass

    def __repr__(self):
        return 'RIP'


def hash_function(key, n):
    """key is an integer and n is 50 times some power of 2. If the load
    factor k / n is greater than 0.7 then n will be doubled."""
    return (key * key + key) % n


def probe_function(key, n):
    """The function P(x) = (x + 3) mod n handles collisions.  We cycle
    through by 3's since gcd(3, n) = 1."""
    return (key + 3) % n


class HashMap:
    """Makes a hash table, i.e., an array. Set the load factor threshold
    at 0.7 and the hash is open address. Has insert, lookup, and delete
    functions. The hash function is x^2 + x mod n. Collisions are handled
     by a linear probe P(x) = x + 3 mod n."""
    def __init__(self):  # initialize a list containing 50 empty tuples
        self.array = []
        i = 0
        while i < 50:
            self.array.append(())
            i = i + 1
        self.n = len(self.array)
        self.k = 0

    def double_array_size(self):
        """Creates a new array with twice as many elements. Then inserts
        all of the entries in the old array into the new one."""
        temp = self.array  # save the old array
        self.n = self.n * 2
        self.array = []  # make the new array
        i = 0
        while i < self.n:  # fill the new array with empty tuples
            self.array.append(())
            i = i + 1
        for j in temp:
            if j != () and type(j) is not Tombstone:
                hash_index = hash_function(j[0], self.n)
                while self.array[hash_index] != ():
                    hash_index = probe_function(hash_index, self.n)
                else:
                    self.array[hash_index] = j
        return print('Doubled array size since the load factor was '
                     'greater than 0.69')

    def insert(self, key, value):
        """Checks the load factor before each insertion. Keys need to be
        unique to prevent errors."""
        if self.k / self.n > .69:  # if k / n is greater than the load
            # factor then we need to double the array size
            self.double_array_size()

        hash_index = hash_function(key, self.n)

        while self.array[hash_index] != ():
            if type(self.array[hash_index]) is Tombstone:
                # probe past the tombstone and continue
                hash_index = probe_function(hash_index, self.n)
                continue
            if self.array[hash_index][0] != key:  # collision has occurred
                hash_index = probe_function(hash_index, self.n)
                continue
            break
        self.array[hash_index] = (key, value)
        self.k = self.k + 1  # record there is one more filled in entry
        return_line = 'Inserted (' + str(key) + ', ' + value + \
                      ') at index ' + str(hash_index)
        # string2 = 'Current load factor is ' + self.k / self.n
        return print(return_line)

    def lookup(self, key):
        """Method that returns the value paired with the given key.
        Implements lazy deletion, i.e., if there are Tombstones found
        during the probing phase the first Tombstone will be replaced
        by the desired (key, value) and the old location will be replaced
         by an empty tuple."""
        hash_index = hash_function(key, self.n)
        tomb_discovered = -1
        key_found = -1
        while self.array[hash_index] != ():  # cycle through filled/
            # Tombstone entries. Since there are always empty entries
            # (because the load factor is not allowed to be > 0.69) and
            # the cycle visits every entry in turn the while loop will
            # eventually terminate
            if type(self.array[hash_index]) is Tombstone:
                if tomb_discovered < 0:  # records index of first
                    # Tombstone encountered
                    tomb_discovered = hash_index
                hash_index = probe_function(hash_index, self.n)
                continue
            if self.array[hash_index][0] != key:
                hash_index = probe_function(hash_index, self.n)
                continue
            else:
                key_found = 1
                break
        if tomb_discovered > -1:
            self.array[tomb_discovered] = self.array[hash_index]
            self.array[hash_index] = ()
            hash_index = tomb_discovered
        if key_found > 0:
            return print('The value associated with key', key, 'is',
                         self.array[hash_index][1], 'at index',
                         hash_index)
        else:
            return print('The value associated with key', key,
                         'was not found')

    def remove(self, key):
        """Removes an entry and replaces with a Tombstone object."""
        hash_index = hash_function(key, self.n)
        while self.array[hash_index] != ():
            if type(self.array[hash_index]) is Tombstone:
                hash_index = probe_function(hash_index, self.n)
                continue
            if self.array[hash_index][0] == key:
                temp = self.array[hash_index]
                self.array[hash_index] = Tombstone()
                return print('Removed the key-value pair', temp,
                             'and placed "RIP"')
            else:
                hash_index = probe_function(hash_index, self.n)
        return print('Unable to remove', key, 'because not found')


h_map = HashMap()
h_map.insert(3, 'hello')
h_map.insert(2, 'hello2')
h_map.insert(1, 'hello3')
h_map.insert(5, 'hello4')
h_map.insert(30, '1st collision')
h_map.insert(180, '2nd collision')
h_map.remove(30)
print(h_map.array)  # verify that the tombstone works
h_map.lookup(180)
print(h_map.array)  # verify that lookup() erases tombstone, relocates
# entry, erases old entry
i = 0
while i < 31:
    h_map.insert(i, str(i))
    i = i + 1
    if i == 30 or i == 31:  # verify that when load factor is > .69 that
        # array size is properly doubled and entries are relocated
        print(h_map.array, h_map.k / h_map.n)
h_map.lookup(3)
h_map.lookup(31)
