import { execFile } from 'child_process';
import cors from 'cors';
import express from 'express';
import helmet from 'helmet';
import path from 'path';

const PORT = process.env.PORT || 8080;

const app = express();

app.use(
  helmet({
    contentSecurityPolicy: {
      useDefaults: true,
      directives: {
        'connect-src': ['*'],
      },
    },
  })
);
app.use(cors());
app.use(express.json());

function convert_url_to_file(glb_url) {
  const parts = glb_url.split('/')
  const refOrganIndex = parts.indexOf('ref-organ');
  return refOrganIndex !== -1 ? parts[refOrganIndex + 1] : undefined;
}

app.post('/mesh-3d-cell-population', (req, res) => {
  // parse post request
  if (req.is('application/json')) {
    const data = req.body;
    const glbFileUrl = data.file ?? '';
    const glbFile = convert_url_to_file(glbFileUrl);
    const sceneNode = data.file_subpath;
    const numNodes = data.num_nodes;

    if (glbFile && data.node_distribution) {
      const nodeDistribution = data.node_distribution;

      // Construct command line to run generate_cell_ctpop
      let cmd = [glbFile, sceneNode];
      for (let [k, v] of Object.entries(nodeDistribution)) {
        cmd.push(k, Math.floor(v * numNodes).toString());
      }

      // Invoke compiled exe.
      execFile('./generate_cell_ctpop', cmd, (error, csvData, stderr) => {
        if (error) {
          console.log(`error: ${error.message} ${stderr}`);
          res.status(500).send('Error processing');
          return;
        }
        // Output csv as response
        res.setHeader('Content-Type', 'text/csv');
        res.setHeader('Content-Disposition', 'attachment; filename=download.csv');
        res.send(csvData.trimEnd());
      });
    } else {
      res.status(400).send('Malformed JSON. node_distribution is a required field.');
    }
  } else {
    res.status(400).send('Only application/json content type is supported.');
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}/mesh-3d-cell-population`);
});
