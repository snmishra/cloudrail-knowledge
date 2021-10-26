
resource "google_compute_instance" "gce-3" {
  name         = "gce-3"
  machine_type = "n1-standard-1"
  zone         = "us-west1-a"
  project     = "dev-for-tests"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  // Local SSD disk
  scratch_disk {
    interface = "SCSI"
  }

  network_interface {
    network = "default"
  }
}


resource "google_compute_instance" "gce-4" {
  name         = "gce-4"
  machine_type = "n1-standard-1"
  zone         = "us-west1-a"
  project     = "dev-for-tests"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  // Local SSD disk
  scratch_disk {
    interface = "SCSI"
  }

  network_interface {
    network = "default"
  }
}
