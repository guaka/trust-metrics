typedef struct _PageRank PageRank;
typedef struct _PageRankPriv PageRankPriv;

struct _PageRank {
  int n_nodes;
  int n_nodes_max;
  int *n_succs;
  int *n_succs_max;
  int **succs;
  int *capacity;

  GHashTable *node_id; /* maps node objects to node numbers */

  char **names; /* maps node numbers to names */
};

PageRank *
page_rank_new (void);

void
page_rank_free (PageRank *self);

gint
page_rank_find_node (PageRank *self, const char *name);

char *
page_rank_node_name (PageRank *self, int node);

void
page_rank_add_edge (PageRank *self, const char *src, const char *dst);

double *
page_rank_compute (PageRank *self, gint seed, double damping);
