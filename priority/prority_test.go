package priority

import (
	"bytes"
	"io"
	"os/exec"
	"runtime"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

func TestStartProcessWithPriority(t *testing.T) {

	// Run these 3 tests inside one test, so we don't have any concurrency issue
	t.Run("WithNormalPriority", func(t *testing.T) {
		err := SetClass(Normal)
		if err != nil {
			t.Error(err)
		}

		output, err := runChildProcess()
		if err != nil {
			t.Fatal(err)
		}
		t.Log(output)
		if runtime.GOOS == "windows" {
			assert.Contains(t, output, "Priority class: NORMAL")
		} else {
			assert.Contains(t, output, "Priority: 0")
		}
	})
	time.Sleep(30 * time.Millisecond)

	t.Run("WithLowerPriority", func(t *testing.T) {
		err := SetClass(Low)
		if err != nil {
			t.Error(err)
		}

		output, err := runChildProcess()
		if err != nil {
			t.Fatal(err)
		}
		t.Log(output)
		if runtime.GOOS == "windows" {
			assert.Contains(t, output, "Priority class: BELOW_NORMAL")
		} else {
			assert.Contains(t, output, "Priority: 10")
		}
	})
	time.Sleep(30 * time.Millisecond)

	t.Run("WithBackgroundPriority", func(t *testing.T) {
		err := SetClass(Background)
		if err != nil {
			t.Error(err)
		}

		output, err := runChildProcess()
		if err != nil {
			t.Fatal(err)
		}
		t.Log(output)
		if runtime.GOOS == "windows" {
			assert.Contains(t, output, "Priority class: IDLE")
		} else {
			assert.Contains(t, output, "Priority: 15")
		}
	})
	time.Sleep(30 * time.Millisecond)
}

func runChildProcess() (string, error) {
	cmd := exec.Command("go", "run", "./check")
	buffer := &bytes.Buffer{}
	cmd.Stdout = buffer
	cmd.Stderr = buffer
	if err := cmd.Run(); err != nil {
		return "", err
	}
	output, err := io.ReadAll(buffer)
	if err != nil {
		return "", err
	}
	return string(output), nil
}
