class Tombstone:
    """Holds the spot of deleted entries.  Prevents unwanted errors during
     lookup."""
    def __init__(self):
        pass

    def __repr__(self):
        return 'RIP'


def hash_function(key, n):
    """key is an integer and n is a power of 2.  If the load factor
    k / n is greater than 0.7 then n will be doubled. """
    return (key * key + key) % n


def probe_function(key, n):
    return (key + 3) % n


class HashMap:
    """Makes a hash table, i.e., an array. Set the load factor threshold
    at 0.7 and the hash is open address. Has insert, lookup, and delete
    functions. The hash function is x^2 + x mod n. Collisions are handled by a
    linear probe P(x) = x + 3 mod n."""

    def __init__(self):  # initialize with a list containing 50 empty tuples
        self.array = []
        i = 0
        while i < 50:
            self.array.append(())
            i = i + 1
        self.n = len(self.array)
        self.k = 0

    def double_array_size(self):
        temp = self.array  # save the old array
        self.n = self.n * 2
        self.array = []  # make the new array
        i = 0
        while i < self.n:  # fill the new array with empty tuples
            self.array.append(())
            i = i + 1
        for j in temp:
            if j != () and type(j) is not Tombstone:
                hash_index = hash_function(j[0])
                while self.array[hash_index] != ():  # a collision has occurred
                    hash_index = probe_function(hash_index, self.n)
                else:
                    self.array[hash_index] = j

    def insert(self, key, value):
        if self.k / self.n > .69:  # if k / n is greater than the load
            # factor then we need to double the array size
            self.double_array_size()

        hash_index = hash_function(key, self.n)
        while self.array[hash_index] != () and \
                self.array[hash_index][0] != key:  # a collision has occurred
            hash_index = probe_function(hash_index, self.n)
        else:
            self.array[hash_index] = (key, value)
        self.k = self.k + 1  # record there is one more filled in entry
        return_line = 'Inserted (' + str(key) + ', ' + value + ') at index ' + str(hash_index)
        # string2 = 'Current load factor is ' + self.k / self.n
        return print(return_line)

    def get_value(self, key):
        hash_index = hash_function(key, self.n)
        tomb_discovered = -1
        while self.array[hash_index] != ():  # a collision has occurred
            if type(self.array[hash_index]) is Tombstone and tomb_discovered < 0:
                tomb_discovered = self.array[hash_index]
            if self.array[hash_index][0] != key:
                hash_index = probe_function(hash_index, self.n)
            else:
                if tomb_discovered > -1:
                    self.array[tomb_discovered] = self.array[hash_index]
                    self.array[hash_index] = ()
                    hash_index = tomb_discovered
                return print('The value associated with key', key, 'is', self.array[hash_index][1])
        return print('Key was not found')

    def remove(self, key):
        hash_index = hash_function(key, self.n)
        while self.array[hash_index] != ():
            if self.array[hash_index][0] == key:
                temp = self.array[hash_index]
                self.array[hash_index] = Tombstone()
                return print('Removed the key-value pair', temp)


h_map = HashMap()
h_map.insert(3, 'hello')
h_map.insert(2, 'hello2')
h_map.insert(1, 'hello3')
h_map.insert(5, 'hello4')
h_map.insert(30, 'hello5')
h_map.get_value(3)
h_map.get_value(30)
h_map.remove(30)
print(h_map.array)
# tomb1 = Tombstone()
# tomb2 = Tombstone()
# print(type(tomb1))
# print(type(tomb2))
# if type(tomb2) is Tombstone:
#     print('true')
# else:
#     print('not true')