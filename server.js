import { exec } from 'child_process';
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

app.post('/mesh-3d-cell-population', (req, res) => {
  // parse post request
  if (req.is('application/json')) {
    const data = req.body;
    const glbFileUrl = data.file;
    const glbFile = path.basename(glbFileUrl);
    const glbStem = path.parse(glbFile).name;
    const sceneNode = data.file_subpath;
    const numNodes = data.num_nodes;

    if (data.node_distribution) {
      const nodeDistribution = data.node_distribution;

      // Construct command line to run generate_cell_ctpop
      let cmd = ['./generate_cell_ctpop', glbStem, sceneNode];
      for (let [k, v] of Object.entries(nodeDistribution)) {
        cmd.push(`"${k}"`, Math.floor(v * numNodes).toString());
      }

      // Invoke compiled exe.
      exec(cmd.join(' '), (error, csvData, stderr) => {
        if (error) {
          console.log(`error: ${error.message} ${stderr}`);
          res.status(500).send('Error processing');
          return;
        }
        // Output csv as response
        res.setHeader('Content-Type', 'text/csv');
        res.setHeader('Content-Disposition', 'attachment; filename=download.csv');
        res.send(csvData);
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
