from faker import Faker
import random


def gen_list_persons(n_persons: int, my_fake: Faker, counter: int) -> tuple[dict, int]:
    """Generate a list of persons in the shape of a dictionnary with:
    {key=id: value=name}.

    Args:
        n_persons (int): Number of persons
        my_fake (Faker): Faker generator
        counter (int): Counter for unique id

    Returns:
        dict: List of persons
        int: Counter modified
    """
    persons = dict()
    for _ in range(n_persons):
        persons[counter] = my_fake.name()
        counter += 1
    return persons, counter


def gen_list_organizations(
    n_orgs: int, my_fake: Faker, counter: int
) -> tuple[dict, int]:
    """Generate a list of organizations in the shape of a dictionnary with:
    {key=id: value=name}.

    Args:
        n_orgs (int): Number of organizations
        my_fake (Faker): Faker generator
        counter (int): Counter for unique ids

    Returns:
        dict: List of organizations
        int: Counter modified
    """
    organizations = dict()
    for _ in range(n_orgs):
        company = my_fake.company()
        if company not in organizations.values():
            organizations[counter] = company
            counter += 1
    return organizations, counter


def gen_list_papers(n_papers: int, my_fake: Faker, counter: int) -> tuple[dict, int]:
    """Generate a list of papers in the shape of a dictionnary with:
    {key=id, value=name}.

    Args:
        n_papers (int): Number of papers
        my_fake (Faker): Faker generator
        counter (int): Counter for unique ids

    Returns:
        dict: List of papers
        int: Counter modified
    """
    papers = dict()
    for _ in range(n_papers):
        papers[counter] = my_fake.sentence(nb_words=10)
        counter += 1
    return papers, counter


def compl_nodes(nodes: list[dict], dicts_to_append: list[dict], label: str) -> None:
    """Append some dictionnaries to the list of nodes **nodes**.
    Convert in the shape:
    {id: dict_key, label:**label**, name:dict_value}

    Args:
        nodes (list[dict]): List of nodes
        dicts_to_append (list[dict]): List of dictionnaries in the shape {key=id: value=name}
        label (str): Lable to use

    Returns:
        None
    """
    for my_dict in dicts_to_append:
        for id, name in my_dict.items():
            nodes.append({"id": id, "label": label, "name": name})

            # Pollute the dataset
            if id == 8374:
                nodes.append({"id": id, "label": label, "name": "Parasite1"})
            elif id == 248549:
                nodes.append({"id": id, "label": label, "name": "Parasite2"})
            elif id == 574643:
                nodes.append({"id": id, "label": label, "name": "Parasite3"})
            elif id == 621345:
                nodes.append({"id": id, "label": label, "name": "Parasite4"})
            elif id == 834564:
                nodes.append({"id": id, "label": label, "name": "Parasite5"})

    return None


def gen_list_works_at(
    edges: list[dict],
    lists_persons: list[dict],
    lists_orgs: list[list[int]],
) -> None:
    """Append some edges with 'works at' relations in the shape:
    {src: id_person, dst: id_org, type: 'works at'}

    Args:
        edges (list[dict]): List of edges
        lists_persons (list[dict]): List of persons
        lists_orgs (list[list[int]]): List of organizations ids

    Returns:
        None
    """

    assert len(lists_persons) == len(lists_orgs)
    for i in range(len(lists_persons)):
        seq = [j for j in range(len(lists_persons))]
        seq.pop(i)
        gen_list_works_at_per_person_list(
            edges,
            lists_persons[i],
            lists_orgs[i],
            [lists_orgs[j] for j in seq],
        )
    return None


def gen_list_works_at_per_person_list(
    edges: list[dict],
    persons: dict,
    probable_orgs: list[int],
    other_orgs: list[list[int]],
) -> None:
    """Generate the list of "works at" relations for
    the list of **persons**. Give higher probability to
    organizations listed in **probable_orgs** than those
    listed in **other_orgs**.

    Args:
        edges (list[dict]): List of edges
        persons (dict): List of persons
        probable_orgs (list[int]): List of organizations ids (appearing with higher probability)
        other_orgs (list[list[int]]): List of organizations ids (appearing with lower probability)

    Returns:
        None
    """

    assert len(other_orgs) == 5

    for p in persons.keys():
        my_dict = dict()

        randn = random.random()
        if randn <= 0.5:
            o = random.choice(probable_orgs)
        elif randn <= 0.6:
            o = random.choice(other_orgs[0])
        elif randn <= 0.7:
            o = random.choice(other_orgs[1])
        elif randn <= 0.8:
            o = random.choice(other_orgs[2])
        elif randn <= 0.9:
            o = random.choice(other_orgs[3])
        else:
            o = random.choice(other_orgs[4])

        my_dict["src"] = p
        my_dict["dst"] = o
        my_dict["type"] = "works_at"

        edges.append(my_dict)
    return None


def gen_list_has_written(
    edges: list[dict],
    n_new_edges: list[int],
    lists_persons: list[list[int]],
    lists_papers: list[list[int]],
) -> None:
    """Append some edges with 'has written' relations in the shape:
    {src: id_person, dst: id_paper, type: 'has written'}

    Args:
        edges (list[dict]): List of edges
        n_new_edges list(int): Number of new edges per list of persons
        lists_persons (list[list[int]]): Lists of person ids
        lists_papers (list[list[int]]): Lists of paper ids

    Returns:
        None
    """

    assert len(lists_persons) == len(lists_papers)
    assert len(lists_persons) == len(n_new_edges)
    for i in range(len(lists_persons)):
        gen_list_has_written_per_person_list(
            edges,
            n_new_edges[i],
            lists_persons[i],
            lists_papers[0],
            [lists_papers[i]],
        )
    return None


def gen_list_has_written_per_person_list(
    edges: list[dict],
    n_new_edges: int,
    persons: list[int],
    probable_papers: list[int],
    other_papers: list[list[int]],
) -> None:
    """Generate a list of "has writtent" relations between
    the **persons** listed and the papers listed in **probable_papers**
    and **other_papers**. A paper in **probable_papers** have better chance to be
    picked up than the papers in **other_papers**.

    Args:
        edges (list[dict]): List of edges
        n_new_edges (int): Number of requested new edges
        persons (list[int]): List of persons
        probable_papers (list[int]): List of papers ids (with higher probability to be picked up)
        other_papers (list[list[int]]): List of papers ids (with lower probability to be picked up)

    Returns:
        None
    """

    assert len(other_papers) == 1

    for _ in range(n_new_edges):
        my_dict = dict()

        p = random.choice(persons)
        randn = random.random()
        if randn <= 0.6:
            o = random.choice(probable_papers)
        else:
            o = random.choice(other_papers[0])

        my_dict["src"] = p
        my_dict["dst"] = o
        my_dict["type"] = "has_written"

        edges.append(my_dict)
    return None


def gen_list_has_read(
    edges: list[dict],
    n_new_edges: list[int],
    lists_persons: list[list[int]],
    lists_papers: list[list[int]],
) -> None:
    """Append some edges with 'has read' relations in the shape:
    {src: id_person, dst: id_paper, type: 'has read'}

    Args:
        edges (list[dict]): List of edges
        n_new_edges list(int): Number of new edges per list of persons
        lists_persons (list[list[int]]): Lists of person ids
        lists_papers (list[list[int]]): Lists of paper ids

    Returns:
        None
    """

    assert len(lists_persons) == len(lists_papers)
    for i in range(len(lists_persons)):
        gen_list_has_read_per_person_list(
            edges,
            n_new_edges[i],
            lists_persons[i],
            lists_papers[0],
            [lists_papers[i]],
        )
    return None


def gen_list_has_read_per_person_list(
    edges: list[dict],
    n_new_edges: int,
    persons: list[int],
    probable_papers: list[int],
    other_papers: list[list[int]],
) -> None:
    """Generate a list of "has read" relations between
    the **persons** listed and the papers listed in **probable_papers**
    and **other_papers**. A paper in **probable_papers** have better chance to be
    picked up than the papers in **other_papers**.

    Args:
        edges (list[dict]): List of edges
        n_new_edges (int): Number of requested new edges
        persons (list[int]): List of persons
        probable_papers (list[int]): List of papers ids (with higher probability to be picked up)
        other_papers (list[list[int]]): List of papers ids (with lower probability to be picked up)

    Returns:
        None
    """

    assert len(other_papers) == 1

    for _ in range(n_new_edges):
        my_dict = dict()

        p = random.choice(persons)
        randn = random.random()
        if randn <= 0.8:
            o = random.choice(probable_papers)
        else:
            o = random.choice(other_papers[0])

        my_dict["src"] = p
        my_dict["dst"] = o
        my_dict["type"] = "has_read"

        edges.append(my_dict)
    return None
