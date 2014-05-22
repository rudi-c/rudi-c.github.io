import math
import sys

EPSILON = 0.001

def float_equal(f1, f2):
    return abs(f1 - f2) <= EPSILON

def float_less_than(f1, f2):
    return f1 < f2 and not float_equal(f1, f2)

def next_power_of_two(f):
    """Get the next integer power of two greater than f."""
    n = 1
    while (n < f):
        n = n << 1
    return n

def distance(p1, p2):
    """Calculate distance between two points."""
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    return math.sqrt(dx * dx + dy * dy)

class Topic(object):
    def __init__(self, input_line):
        self.id = int(input_line[0])
        self.x = float(input_line[1])
        self.y = float(input_line[2])
        self.p = (self.x, self.y)
        self.questions = []

    def question_count(self):
        return len(self.questions.items)

class Question(object):
    def __init__(self, input_line):
        self.id = int(input_line[0])
        self.topics = [int(id) for id in input_line[2:]]
        # assert (int(input_line[1]) == len(self.topics))

class Gatherer(object):
    def is_full(self):
        """Returns whether we've acquired as many queries as requested."""
        return self.query_size < len(self.results)

    def distance_to_furthest(self):
        """Returns distance to furthest topic gathered so far."""
        return distance(self.results[-1].p, self.location)

class TopicGatherer(Gatherer):
    """Builds a query asking for topics near a location."""

    def __init__(self, query_size, location):
        self.query_size = query_size
        self.location = location
        # Sorted list of query results
        self.results = []

    def topic_is_smaller(self, topic1, topic2):
        """Returns whether the first topic should appear earlier in the
        query results. Ties in distance are broken by id. Larger ids appear
        earlier.
        """
        d1 = distance(topic1.p, self.location)
        d2 = distance(topic2.p, self.location)
        if float_equal(d1, d2):
            return topic1.id > topic2.id
        else:
            return d1 < d2

    def add_topic(self, topic):
        """Add a topic to the query gatherer."""
        added = False

        # Do a linear search for position in the list of query results
        # in which to insert this topic. We could do binary search, but
        # insertion is linear anyway, so it would only be a minor
        # optimization.
        for i in xrange(len(self.results)):
            if self.topic_is_smaller(topic, self.results[i]):
                self.results.insert(i, topic)
                added = True
                break

        # Append to end if needed.
        if not added:
            self.results.append(topic)

        # Trim list of query results to only keep as many as were demanded.
        if len(self.results) > self.query_size:
            self.results.pop()


class QuestionGatherer(Gatherer):
    def __init__(self, query_size, location, topics_by_id):
        self.query_size = query_size
        self.location = location
        # Sorted list of query results
        self.results = []
        # List of distances of questions we've seen before. We need to keep
        # a list of these because distances are determined by topics, and
        # questions can have multiple topics.
        self.question_distances = {}
        # For getting topics.
        self.topics_by_id = topics_by_id

    def question_is_smaller(self, question1, question2):
        """Returns whether the first question should appear earlier in the
        query results. Ties in distance are broken by id. Larger ids appear
        earlier.
        """
        d1 = self.question_distances[question1]
        d2 = self.question_distances[question2]
        if float_equal(d1, d2):
            return question1.id > question2.id
        else:
            return d1 < d2

    def add_topic(self, topic):
        """Add the questions associated to the topic to the query gatherer."""
        for question in topic.questions:
            # Skip if we already added this question (this can happen since
            # questions have multiple topics)
            if self.question_distances.has_key(question):
                continue

            added = False

            # Do a linear search for position in the list of questions
            # in which to insert this question. We could do a binary search,
            # but insertion is linear anyway, so it would only be a minor
            # optimization.
            question_distance = min(distance(self.topics_by_id[id].p, 
                                             self.location)
                                    for id in question.topics)
            self.question_distances[question] = question_distance
            for i in xrange(len(self.results)):
                if self.question_is_smaller(question, self.results[i]):
                    self.results.insert(i, question)
                    added = True
                    break

            # Append at end if needed.
            if not added:
                self.results.append(question)

            # Trim list of query results to only keep as many as were demanded.
            if len(self.results) > self.query_size:
                self.results.pop()


class Quadtree:
    """A point (x, y) is in the quadtree if xmin <= x < xmax, ymin <= y < ymax
    A given node either contains a single topic, or at least one children (one
    of NE, NW, SE, SW).
    """
    def __init__(self, topics, xmin=None, ymin=None, xmax=None, ymax=None):
        self.contents = None
        self.NW = None
        self.NE = None
        self.SE = None
        self.SW = None
        self.xmin = min(t.x for t in topics)     if xmin is None else xmin 
        self.ymin = min(t.y for t in topics)     if ymin is None else ymin 
        self.xmax = max(t.x for t in topics) + 1 if xmax is None else xmax 
        self.ymax = max(t.y for t in topics) + 1 if ymax is None else ymax 
        if not xmin:
            self._adjust_to_power_of_two()

        # Filter out topics that don't belong in this Quadtree.
        topics = [t for t in topics if self.xmin <= t.x < self.xmax
                                    if self.ymin <= t.y < self.ymax]

        # Check if the location of the remaining topics are all identical.
        # If so, we should terminate here, since splitting the quadtree
        # further is useless.
        all_same = True
        for t in topics:
            if t.x != topics[0].x or t.y != topics[0].y:
                all_same = False
                break

        if (len(topics) == 1 or all_same or
            self.xmax - self.xmin <= 1 or self.ymax - self.ymin <= 1): 
            self.contents = topics
        elif len(topics) > 0:
            # Sort the topics by their bins.
            xcenter = (self.xmax + self.xmin) / 2
            ycenter = (self.ymax + self.ymin) / 2

            self.NW = Quadtree(topics, self.xmin, ycenter, xcenter, self.ymax)
            self.NE = Quadtree(topics, xcenter, ycenter, self.xmax, self.ymax)
            self.SW = Quadtree(topics, self.xmin, self.ymin, xcenter, ycenter)
            self.SE = Quadtree(topics, xcenter, self.ymin, self.xmax, ycenter)

            # Get rid of empty nodes.
            if self.NW.is_empty():
                self.NW = None
            if self.NE.is_empty():
                self.NE = None
            if self.SE.is_empty():
                self.SE = None
            if self.SW.is_empty():
                self.SW = None

    def print_tree(self, indent = 0):
        """For debugging."""
        assert ((self.contents is None) != 
                (self.NW or self.NE or self.SW or self.SE))
        indentation = "  " * indent
        print (indentation + "x : [%d,%d) y : [%d,%d)" % 
                             (self.xmin, self.xmax, self.ymin, self.ymax))
        if self.contents:
            for content in self.contents:
                print indentation + str((content.id, content.x, content.y))
        else:
            if self.SW:
                print indentation + "SW : "
                self.SW.print_tree(indent + 1)
            if self.SE:
                print indentation + "SE : "
                self.SE.print_tree(indent + 1)
            if self.NW:
                print indentation + "NW : "
                self.NW.print_tree(indent + 1)
            if self.NE:
                print indentation + "NE : "
                self.NE.print_tree(indent + 1)

    def _adjust_to_power_of_two(self):
        """Adjust the range of the quadtree such that it is a integer 
        power of two. It is preferable to have integer powers of two to avoid 
        floating-point issues.
        """
        xrange = self.xmax - self.xmin
        yrange = self.ymax - self.ymin
        self.xmin = int(self.xmin - (next_power_of_two(xrange) - xrange) / 2)
        self.xmax = self.xmin + next_power_of_two(xrange)
        self.ymin = int(self.ymin - (next_power_of_two(yrange) - yrange) / 2)
        self.ymax = self.ymin + next_power_of_two(yrange)

    def is_empty(self):
        return not (self.NW or self.NE or self.SE or self.SW or self.contents)

    def contains(self, x, y):
        """Returns if the point (x, y) is within the bounds of this Quadtree"""
        return self.xmin <= x < self.xmax and self.ymin <= y < self.ymax

    def list_children(self, x, y):
        """Return an array of children for this Quadtree. If (x, y) falls in
        one of the child, that child will be the first element of the array.
        """
        children = []
        for child in [self.NW, self.NE, self.SE, self.SW]:
            if child and child.contains(x, y):
                children.append(child)
        for child in [self.NW, self.NE, self.SE, self.SW]:
            if child and not child.contains(x, y):
                children.append(child)
        return children

    def distance_to_bounds(self, p):
        """Returns the distance to the Quadtree (0 if it's inside)"""
        x, y = p
        # Distance to vertical borders (left, right).
        if self.xmin < x < self.xmax:
            dx = 0
        else:
            dx = max(x - self.xmax, self.xmin - x)
        # Distance to horizontal borders (top, bottom).
        if self.ymin < y < self.ymax:
            dy = 0
        else:
            dy = max(y - self.ymax, self.ymin - y)
        return distance(p, (dx, dy))

    def find_closest(self, x, y, gatherer):
        """Find the point in the Quadtree closest to (x, y). An optional
        parameter can be passed as a heuristic to terminate the search early.
        """
        # Check if we should terminate here.
        if (not gatherer.is_full() or not float_less_than(
            gatherer.distance_to_furthest(), self.distance_to_bounds((x, y)))):
            if self.contents:
                # Leaf node, add element at the leaf.
                for content in self.contents:
                    gatherer.add_topic(content)
            else:
                # Look in children.
                children = self.list_children(x, y)
                assert len(children) > 0
                for child in children:
                    child.find_closest(x, y, gatherer)

def main():
    input_line = raw_input().split(" ")
    topic_count = int(input_line[0])
    question_count = int(input_line[1])
    query_count = int(input_line[2])
    topics = []
    questions = []
    queries = []

    # Read topics.
    for _ in xrange(topic_count):
        topics.append(Topic(raw_input().split(" ")))
    topics_by_id = { topic.id : topic for topic in topics }

    # Read questions.
    for _ in xrange(question_count):
        new_question = Question(raw_input().split(" "))
        questions.append(new_question)
        for topic_id in new_question.topics:
            topics_by_id[topic_id].questions.append(new_question)

    quadtree = Quadtree(topics)
    # quadtree.print_tree()

    # Read and execute queries.
    for _ in xrange(query_count):
        elements = raw_input().split(" ")
        count, x, y = int(elements[1]), float(elements[2]), float(elements[3])

        # Check for query type.
        if elements[0] == "t":
            gatherer = TopicGatherer(count, (x, y))
            quadtree.find_closest(x, y, gatherer)
            sys.stdout.write(" ".join(str(topic.id) 
                             for topic in gatherer.results) + "\n")
        else:
            gatherer = QuestionGatherer(count, (x, y), topics_by_id)
            quadtree.find_closest(x, y, gatherer)
            sys.stdout.write(" ".join(str(question.id) 
                             for question in gatherer.results) + "\n")

main()