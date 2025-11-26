import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { GitBranch, AlertCircle, ExternalLink, Download, Heart } from "lucide-react";

interface Neo4jNode {
  model_id: string;
  downloads?: number;
  pipeline_tag?: string | null;
  created_at?: string;
  library_name?: string;
  url?: string;
  likes?: number;
  tags?: string[];
}

interface Neo4jRelationship {
  source: Neo4jNode;
  relationship: string;
  target: Neo4jNode;
}

interface Neo4jData {
  nodes: {
    nodes: Neo4jNode[];
  };
  relationships: {
    relationships: Neo4jRelationship[];
  };
}

interface ModelTreeProps {
  neo4jData: Neo4jData | null;
}

interface ModelNode {
  name: string;
  children?: ModelNode[];
  hasRisk?: boolean;
}

const sampleTree: ModelNode = {
  name: "nvidia/gpt-oss-120b-Eagle3",
  children: [
    {
      name: "openai/gpt-oss-120b",
      children: [
        { name: "base-model-v1", hasRisk: true },
        { name: "base-model-v2" },
      ],
    },
    {
      name: "fine-tuned-model-1",
      children: [
        { name: "derivative-a" },
        { name: "derivative-b", hasRisk: true },
      ],
    },
  ],
};

const TreeNode = ({ node, level = 0 }: { node: ModelNode; level?: number }) => {
  const indent = level * 24;

  return (
    <div className="animate-fade-in">
      <div
        className="flex items-center gap-2 py-2 hover:bg-muted/50 rounded-lg px-2 transition-colors cursor-pointer"
        style={{ marginLeft: `${indent}px` }}
      >
        <GitBranch className="w-4 h-4 text-secondary" />
        <span className="text-sm font-medium">{node.name}</span>
        {node.hasRisk && (
          <Badge variant="destructive" className="text-xs">
            <AlertCircle className="w-3 h-3 mr-1" />
            Risk
          </Badge>
        )}
      </div>
      {node.children && node.children.map((child, index) => (
        <TreeNode key={index} node={child} level={level + 1} />
      ))}
    </div>
  );
};

const Neo4jModelNode = ({ node }: { node: Neo4jNode }) => {
  return (
    <div className="animate-fade-in py-2 px-3 hover:bg-muted/50 rounded-lg transition-colors border border-border mb-2">
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <GitBranch className="w-4 h-4 text-secondary flex-shrink-0" />
            <a
              href={node.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm font-medium hover:text-secondary transition-colors"
            >
              {node.model_id}
            </a>
            <ExternalLink className="w-3 h-3 text-muted-foreground" />
          </div>

          {node.pipeline_tag && (
            <Badge variant="outline" className="text-xs mt-2">
              {node.pipeline_tag}
            </Badge>
          )}

          <div className="flex items-center gap-3 mt-2 text-xs text-muted-foreground">
            {node.downloads !== undefined && (
              <div className="flex items-center gap-1">
                <Download className="w-3 h-3" />
                <span>{(node.downloads || 0).toLocaleString()}</span>
              </div>
            )}
            {node.likes !== undefined && (
              <div className="flex items-center gap-1">
                <Heart className="w-3 h-3" />
                <span>{node.likes}</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

const ModelTree = ({ neo4jData }: ModelTreeProps) => {
  if (!neo4jData || !neo4jData.nodes?.nodes || neo4jData.nodes.nodes.length === 0) {
    return (
      <Card className="bg-card border-border shadow-md">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <GitBranch className="w-5 h-5 text-secondary" />
            Model Lineage Tree
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-muted-foreground">
            <p className="text-sm">No model lineage data yet.</p>
            <p className="text-xs mt-2">Ask about a specific model to see its relationships!</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const nodes = neo4jData.nodes.nodes;
  const relationships = neo4jData.relationships?.relationships || [];

  return (
    <Card className="bg-card border-border shadow-md">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <GitBranch className="w-5 h-5 text-secondary" />
          Model Lineage ({nodes.length} models)
        </CardTitle>
      </CardHeader>
      <CardContent className="max-h-[500px] overflow-y-auto">
        <div className="space-y-2">
          {nodes.map((node, index) => (
            <Neo4jModelNode key={index} node={node} />
          ))}
        </div>

        {relationships.length > 0 && (
          <div className="mt-4 pt-4 border-t border-border">
            <h4 className="text-sm font-medium mb-2">Relationships ({relationships.length})</h4>
            <div className="space-y-1 text-xs">
              {relationships.map((rel, index) => (
                <div key={index} className="flex items-center gap-2 text-muted-foreground">
                  <span className="font-mono">{rel.source.model_id}</span>
                  <Badge variant="secondary" className="text-xs">
                    {rel.relationship}
                  </Badge>
                  <span className="font-mono">{rel.target.model_id}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="mt-4 pt-4 border-t border-border">
          <div className="flex items-center gap-4 text-xs text-muted-foreground">
            <div className="flex items-center gap-1">
              <Download className="w-3 h-3" />
              <span>Downloads</span>
            </div>
            <div className="flex items-center gap-1">
              <Heart className="w-3 h-3" />
              <span>Likes</span>
            </div>
            <div className="flex items-center gap-1">
              <ExternalLink className="w-3 h-3" />
              <span>View on HuggingFace</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default ModelTree;
