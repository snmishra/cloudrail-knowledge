
resource "google_compute_instance" "gce-1" {
  name         = "gce-1"
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

  metadata = {
    serial-port-enable = true
  }
}


resource "google_compute_instance" "gce-2" {
  name         = "gce-2"
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

  metadata = {
    serial-port-enable = true
  }
}
