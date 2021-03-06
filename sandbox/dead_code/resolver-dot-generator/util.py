# Copyright: 2006 Brian Harring <ferringb@gmail.com>
# License: GPL2/BSD

def mangle_name(arg):
	return '"%s"' % str(arg).replace('"', '\\"')

def dump_edge(parent, child, text):
	return "%s->%s [label=%s];" % (mangle_name(parent), mangle_name(child), mangle_name(text))

def dump_dot_file_from_graph(graph, filepath, graph_name="dumped_graph"):
	if isinstance(filepath, basestring):
		fd = open(filepath, "w")
	else:
		fd = filepath
	if not hasattr(fd, "write"):
		raise TypeError("filepath must be either a file instance or a string filepath: got %s" % filepath)
	fd.write("digraph %s {\n" % graph_name)
	for a,data in graph.atoms.iteritems():
		for parent in data[0]:
			if data[1]:
				for matches in data[1]:
					fd.write("\t%s\n" % dump_edge(parent, matches, a))
			else:
				fd.write("\t%s\n" % dump_edge(parent, a, a))

	fd.write("\tnode [shape=circle];\n")
	for x in graph.pkgs.keys():
		fd.write("\t%s\n" % mangle_name(x))
#	fd.write("\tnode [shape=circle];\n\t%s;\n" % " ".join(map(mangle_name, graph.pkgs.keys())))
	l = list(graph.unresolved_atoms())
	if l:
		fd.write("\tnode [shape=box];\n\t%s;\n" % " ".join(map(mangle_name, graph.unresolved_atoms())))
		del l
	fd.write("}\n");

