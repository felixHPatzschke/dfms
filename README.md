# dfms (Dark Field Micro-Spectroscopy)
 This is a repository of utilities I intend to use for data analysis in the context of my Master's Thesis.

## Workflows
 This repo, specifically, the `util` package, aims to keep in one place the resources I use for multiple steps in analysing lab data. 
 Corresponding to each of these steps, there is one file in the top level directory, usually a Jupyter Notebook, through which is is performed.
 
### Device Ingest
 File: `Devices Ingest.ipynb`
 
 This step simply reads raw data (in CSV format) that specify the characteristic spectrum of devices that are (or may be) used in the lab setup, builds interpolation functions and an error estimations, packages these together with some other information about the devices and stores this information serialized in files, one file corresponding to one device.
 
 These data are later used to correct the measured spectrum of a particle for the signature of the setup.
 
 Currently, the following devices and corresponding spectra are available:
 <figure>
   <img src="https://github.com/felixHPatzschke/dfms/blob/main/Devices Characteristic Spectra.png">
   <figcaption><figcaption>
 <figure>
 
### Calibration
 File: `Calibration.ipynb`
 
 The spectral information in the microscope images comes from a diffraction grating that is placed in front of the camera sensor.
 This generates a displaced first-order image of any object. 
 How far this image is displaced from the zero-th order depends on the density of the grating, its distance from the camera sensor and the wavelength of the light creating the image. 
 Hence, if an image is made up of not just one wavelength of light, its first-order image will be smeared out in a sort of "streak". 
 
 To recover spectral information from this streak, one needs only to convert the distance of a point (in pixels) from the original image to the corresponding wavelength.
 I find, the easiest way to accomplish this is to create and image/first-order pair with only one wavelength, measure the displacement and save the linear conversion factor between the two.
 To this end, I focus a laser spot (λ=532 nm) on a cover slide and let the reflection make an image on the camera sensor, with the diffraction grating installed, creating a second spot.
 
 The Jupyter Notebook then reads the generated microscope video, finds the spots via a fit to a 2D Gauss curve, calculates their distance, and from that the pixels-to-wavelength conversion factor.
 
 In addition, the diffraction grating is mounted in a THORLABS screwable lens tube (see https://www.thorlabs.com/navigation.cfm?guide_id=74). This makes it convenient to remove the grating from setup for other measurements as well as rotate it to move the streaks in the microscope image to different angles, while keeping the distance of the grating from the sensor somewhat reproducible. Of course, since it screws in to and out of the camera's front plate, the distance between grating and sensor changes depending on its orientation.
 
 The Jupyter Notebook also computes the angle to which the grating is screwed in from the spots. 
 (Provisions for manual corrections for full rotations, which obviously can't be detected easily, are made.)
 This allows for a linear fit, screw-in angle vs calibration factor, whose parameters are saved to file, along with an error estimate.
 
### Particle Tagging
 File: `Tagging.py`
 
 This goal of this step is to generate Descriptor files to tell the final evaluation script everything it needs to know about the particle that it is to analyze. This includes, among others
 * which video files the particle appears in
 * at which position it is
 * the screw-in angle of the diffraction grating
 * devices used for the measurement that warrant a spectral correction

 This step requires the user to locate and select a feature in an image, hence, an executable python file and a Qt-based GUI are used here, instead of a Jupyter Notebook.
 
 After the user puts in the information about the particle, is is serialized to a JSON file.
 
### Analysis of Particle Spectra 
 File: `Spectra Analysis.ipynb`
 
 This Jupyter Notebook performs the final evaluation of a particle's scattering spectrum.
 Particle metadata is read from JSON files placed in a directory that is specified at the baginning of the Notebook.
 The microscope data is then read from the video files specified in the metadata.
 Various mathematical things happen to generate spectra corresponding to the light captured from the particle.
 The spectra are corrected for the signatures of the devices used for the measurement of each particle.
 If applicable, they are compared to theoretical scattering spectra.
 
 This step generates some diagrams. These are exported to files.

## Dependencies
 * `numpy 1.20.2` or higher
 * `matplotlib 3.4.2` or higher and `matplotlib-inline 0.1.2` or higher
 * `scipy 1.7.0` or higher
 * `PyQt5 5.15.4` or higher
 * `npTDMS 1.3.0` or higher

## To do

### Quality of Life Features (Particle Tagging)
 * Automatic particle detection
 * A persistent settings file
     + Starting path for the file chooser
     + Colour map for previews
 * Input files from command line arguments
 * Preview
     + Selected region for zero-th order
     + Selected region for the streak
     + An extracted Spectrum from the streak
     + A corrected spectrum given the currently selected devices
 * Allow input of angles outside of the 0°-360° range, specifically negative angles
 
### Calibration
 * Make it possible to save multiple calibrations (e.g. by date of recording), save the appropriate one for each particle in Tagging

### Analysis of Particle Spectra
 * Automatically write the results to CSV files
 * Better (i.e. weighted) normalization for the comparison to theory
  
and many, many more...
